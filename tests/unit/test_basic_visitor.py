#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase

from tapioca.visitor import SimpleVisitor


class VisitorTestCase(TestCase):

    def test_basic_visitor(self):

        class A(object):
            pass

        class BasicVisitor(SimpleVisitor):
            def __init__(self):
                self.data = None

            def visit_a(self, node):
                self.data = 'success'

        visitor = BasicVisitor()
        assert visitor.data == None
        visitor.visit(A())
        assert visitor.data == 'success'

    def test_visit_more_classes(self):

        class Foo(object):
            pass

        class Bar(object):
            def __init__(self, left, right):
                self.left = left
                self.right = right

        class BasicVisitor(SimpleVisitor):
            def __init__(self):
                self.data = ''

            def visit_foo(self, node):
                self.data = self.data + 'foo'

            def visit_bar(self, node):
                self.visit(node.left)
                self.data = self.data + 'bar'
                self.visit(node.right)

        structure = Bar(Foo(), Foo())
        visitor = BasicVisitor()
        assert visitor.data == ''
        visitor.visit(structure)
        assert visitor.data == 'foobarfoo'

    def test_visit_none(self):

        class Foo(object):
            pass

        class Bar(object):
            def __init__(self, left, right):
                self.left = left
                self.right = right

        class BasicVisitor(SimpleVisitor):
            def __init__(self):
                self.data = ''

            def visit_foo(self, node):
                self.data = self.data + 'foo'

            def visit_bar(self, node):
                self.visit(node.left)
                self.data = self.data + 'bar'
                self.visit(node.right)

            def visit_nonetype(self, node):
                self.data = self.data + '{NONE}'

        structure = Bar(None, Foo())
        visitor = BasicVisitor()
        assert visitor.data == ''
        visitor.visit(structure)
        assert visitor.data == '{NONE}barfoo'
