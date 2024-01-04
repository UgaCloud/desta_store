from django.db.models import Sum, Count
from django.views.generic import ListView
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse

from pis_product.models import StockOut


class DailyStockLogs(ListView):
    model = StockOut
    template_name = 'logs/daily_stock_logs.html'
    paginate_by = 200
    is_paginated = True

    def __init__(self, *args, **kwargs):
        super(DailyStockLogs, self).__init__(*args, **kwargs)
        self.logs_date = ''
        self.today_date = ''

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))

        return super(
            DailyStockLogs, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        self.logs_date = self.request.GET.get('date')
        if self.logs_date:
            logs_date = self.logs_date.split('-')
            year = logs_date[0]
            month = logs_date[1]
            day = logs_date[2]

            try:
                queryset = StockOut.objects.filter(
                    dated__year=year,
                    dated__month=month,
                    dated__day=day,
                ).values('product__name').annotate(
                    receipt_item=Count('product__name'),
                    total_qty=Sum('stock_out_quantity')
                )
            except:
                queryset = []
        else:
            self.today_date = timezone.now().date()
            queryset = StockOut.objects.filter(
                dated__year=self.today_date.year,
                dated__month=self.today_date.month,
                dated__day=self.today_date.day,
            ).values('product__name').annotate(
                receipt_item=Count('product__name'),
                total_qty=Sum('stock_out_quantity')
            )

        return queryset.order_by('product__name')

    def get_context_data(self, **kwargs):
        context = super(DailyStockLogs, self).get_context_data(**kwargs)
        queryset = self.get_queryset()
        if queryset:
            total = queryset.aggregate(Sum('selling_price'))
            total = total.get('selling_price__sum') or 0
        else:
            total = 0

        context.update({
            'total': total,
            'today_date': (
                timezone.now().strftime('%Y-%m-%d')
                if self.today_date else None),
            'logs_date': self.logs_date,
        })
        return context


class MonthlyStockLogs(ListView):
    model = StockOut
    template_name = 'logs/monthly_stock_logs.html'
    paginate_by = 20
    is_paginated = True
    

    def __init__(self, *args, **kwargs):
        super(MonthlyStockLogs, self).__init__(*args, **kwargs)
        self.month = ''
        self.current_month = ''
        self.year = ''

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))

        return super(
            MonthlyStockLogs, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        self.month = self.request.GET.get('month')
        self.year = self.request.GET.get('year')
        current_date = timezone.now().date()
        
        months = [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ]

        if self.month:
            
            queryset = StockOut.objects.filter(
                dated__year=self.year,
                dated__month=self.month
            ).values('product__name').annotate(
                receipt_item=Count('product__name'),
                total_qty=Sum('stock_out_quantity')
            )

            self.month = months[int(self.month) - 1]

        else:
            self.month = current_date.strftime("%B")
            self.year = current_date.year
            queryset = StockOut.objects.filter(
                dated__year=current_date.year,
                dated__month=current_date.month,
            ).values('product__name').annotate(
                receipt_item=Count('product__name'),
                total_qty=Sum('stock_out_quantity')
            )

        return queryset.order_by('product__name')

    def get_context_data(self, **kwargs):
        context = super(MonthlyStockLogs, self).get_context_data(**kwargs)
        queryset = self.get_queryset()
        if queryset:
            total = queryset.aggregate(Sum('selling_price'))
            total = total.get('selling_price__sum') or 0
        else:
            total = 0

        context.update({
            'total': total,
            'month': self.month,
            'year': self.year
        })
        return context

class BetweenDatesStockLogs(ListView):
    model = StockOut
    template_name = 'logs/between_dates.html'
    paginate_by = 20
    is_paginated = True
    

    def __init__(self, *args, **kwargs):
        super(BetweenDatesStockLogs, self).__init__(*args, **kwargs)
        self.from_date = ''
        self.to_date = ''

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))

        return super(
            BetweenDatesStockLogs, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        self.from_date = self.request.GET.get('from_date')
        self.to_date = self.request.GET.get('to_date')
        current_date = timezone.now().date()
        
        if self.from_date:
            # logs_date = self.logs_date.split('-')
            # year = logs_date[0]
            # month = logs_date[1]
            # day = logs_date[2]
            
            queryset = StockOut.objects.filter(
                dated__range= [self.from_date,self.to_date]
            ).values('product__name').annotate(
                receipt_item=Count('product__name'),
                total_qty=Sum('stock_out_quantity')
            )

        else:
            self.from_date = current_date
            self.to_date = current_date
            queryset = StockOut.objects.filter(
                dated__range = [current_date,current_date]
            ).values('product__name').annotate(
                receipt_item=Count('product__name'),
                total_qty=Sum('stock_out_quantity')
            )

        return queryset.order_by('product__name')

    def get_context_data(self, **kwargs):
        context = super(BetweenDatesStockLogs, self).get_context_data(**kwargs)
        queryset = self.get_queryset()
        if queryset:
            total = queryset.aggregate(Sum('selling_price'))
            total = total.get('selling_price__sum') or 0
        else:
            total = 0

        context.update({
            'total': total,
            'from-date': self.from_date,
            "to-date": self.to_date
        })
        return context