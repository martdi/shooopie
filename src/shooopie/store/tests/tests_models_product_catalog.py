from django.test import TestCase
from store.models import Product, ProductStatus, Tag, Category

# Create your tests here.
class ProductTestCase(TestCase):
    def setUp(self):
        gizmo = Product.objects.create(
            name='gizmo',
            description='This is a gizmo.',
            slug='gizmo',
            price=10.00,
            status_id=ProductStatus.PUBLISHED,
        )
        
        gizmo2 = Product.objects.create(
            name='gizmo 2',
            description='This is the second gizmo.',
            slug='gizmo2',
            price=12.00,
            status_id=ProductStatus.DRAFT,
        )

        new = Tag.objects.create(name='New gizmo')
        new2 = Tag.objects.create(name='New gizmo 2')

        cat = Category.objects.create(name='New category')
        cat2 = Category.objects.create(name='New category 2')

        cat.products.add(gizmo)
        cat2.products.add(gizmo2)

        new.products.add(gizmo)
        new2.products.add(gizmo2)

    def test_query_products_by_category(self):
        cat = Category.objects.get(name='New category')
        gizmo = Product.objects.get(name='gizmo')

        self.assertEqual(1, Product.objects.filter(categories=cat).count())
        self.assertEqual(gizmo, Product.objects.filter(categories=cat).first())
        self.assertEqual(gizmo, Product.objects.by_category_name('New category').first())

    def test_query_exclude_products_by_category(self):
        cat = Category.objects.get(name='New category')
        gizmo2 = Product.objects.get(name='gizmo 2')

        self.assertEqual(1, Product.objects.exclude(categories=cat).count())
        self.assertEqual(gizmo2, Product.objects.exclude(categories=cat).first())
        self.assertEqual(gizmo2, Product.objects.exclude_by_category_name('New category').first())

    def test_query_products_by_tag(self):
        tag = Tag.objects.get(name='New gizmo 2')
        gizmo2 = Product.objects.get(name='gizmo 2')
        self.assertEqual(1, Product.objects.filter(tags=tag).count())
        self.assertEqual(gizmo2, Product.objects.filter(tags=tag).first())
        self.assertEqual(gizmo2, Product.objects.by_tag_name('New gizmo 2').first())

    def test_query_exclude_products_by_tag(self):
        tag = Tag.objects.get(name='New gizmo')
        gizmo2 = Product.objects.get(name='gizmo 2')

        self.assertEqual(1, Product.objects.exclude(tags=tag).count())
        self.assertEqual(gizmo2, Product.objects.exclude(tags=tag).first())
        self.assertEqual(gizmo2, Product.objects.exclude_by_tag_name('New gizmo').first())


    def test_products_in_catalog_only_select_published(self):
        Product.objects.create(
            name='Gizmo 3',
            description='Another gizmo',
            status_id=ProductStatus.DISCONTINUED,
            price=15.0,
            slug='g3'
        )

        self.assertEqual(1, Product.objects.in_catalog().count())

    def test_deleting_product_marks_as_discontinued(self):
        gizmo2 = Product.objects.get(name='gizmo 2')
        id = gizmo2.id
        gizmo2.delete()

        deleted_gizmo = Product.objects.get(pk=id)
        self.assertIsNotNone(deleted_gizmo)
        self.assertEqual(ProductStatus.DISCONTINUED, deleted_gizmo.status_id)

    def test_deleting_product_from_queryset_marks_as_discontinued(self):
        Product.objects.all().delete()
        self.assertEqual(2, Product.objects.count())
        self.assertEqual(ProductStatus.DISCONTINUED, Product.objects.first().status_id)