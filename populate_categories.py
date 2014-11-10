# -*- coding: utf-8 -*-
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop_project.settings')
import xlrd

import django

from store.models import Category, Product
django.setup()


def populate():
    xl_book = xlrd.open_workbook('data.xlsx', 'rb')
    xl_sheet = xl_book.sheet_by_index(1)
    main_category = Category(id=1, name='main', parent_category=None, image_link='-', level=0)
    main_category.save()
    for cat_row in xrange(5, xl_sheet.nrows):
        cat_id = int(xl_sheet.cell(cat_row, 0).value)
        cat_title = xl_sheet.cell(cat_row, 1).value
        cat_parent_id = xl_sheet.cell(cat_row, 2).value
        print(cat_title)

        try:
            cat_image_link = xl_sheet.cell(cat_row, 3).value
        except IndexError:
            cat_image_link = 'http://www.clipartbest.com/cliparts/dc7/5dR/dc75dRdc9.jpeg'

        if cat_parent_id:
            parent_category = Category.objects.get(pk=cat_parent_id)
        else:
            parent_category = main_category

        cat_level = parent_category.level + 1

        category = Category(id=cat_id,
                            name=cat_title,
                            parent_category=parent_category,
                            image_link=cat_image_link,
                            level=cat_level)
        category.save()


def main():
    Product.objects.all().delete()
    Category.objects.all().delete()
    populate()


if __name__ == "__main__":
    main()
