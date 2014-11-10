# -*- coding: utf-8 -*-
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop_project.settings')
import xlrd

import django

from store.models import Category, Product
import random

django.setup()


def populate():
    xl_workbook = xlrd.open_workbook('data.xlsx')
    xl_sheet = xl_workbook.sheet_by_index(0)

    for row_idx in xrange(2, xl_sheet.nrows):

        name = xl_sheet.cell(row_idx, 1).value
        new_name = ""
        for char in name:
            try:
                new_char = char.decode("ascii")
            except UnicodeEncodeError:
                new_char = '?'
            new_name += new_char

        name = new_name

        try:
            category = int(xl_sheet.cell(row_idx, 4).value)
        except:
            category = random.randint(4, 169)

        category = Category.objects.get(pk=category)

        Product.objects.get_or_create(name=name,
            code=xl_sheet.cell(row_idx, 0).value,
            price=float(xl_sheet.cell(row_idx, 2).value),
            quantity=int(xl_sheet.cell(row_idx, 3).value),
            image_link=xl_sheet.cell(row_idx, 6).value,
            category=category,
            description="Мы еще работаем над описанием для этого продукта.")


if __name__ == '__main__':
    Product.objects.all().delete()
    print("Starting population script")
    populate()
