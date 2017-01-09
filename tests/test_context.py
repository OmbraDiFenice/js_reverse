from django.test import TestCase, override_settings
from django.urls.exceptions import NoReverseMatch

from js_reverse.templatetags.js_reverse import build_context
from js_reverse.settings import *

@override_settings(ROOT_URLCONF='js_reverse.tests.urls')
class TestContext(TestCase):
    
    def test_1_context_structure(self):
        context = build_context(ALL_NAMES)
        self.assertIn('patterns', context)
        self.assertIn('object_name', context)
        self.assertEqual(context['object_name'], JS_OBJECT_NAME)
        
    def test_2_name_structure(self):
        context = build_context(ALL_NAMES)
        patterns = context['patterns']
    
        self.assertNotIn('app1_view1', patterns)
        self.assertIn('app1_view2', patterns)
        self.assertNotIn('app1:app1_view2', patterns)
        self.assertIn('app1:app1_view3', patterns)
        
        self.assertIn('app2:app2_view1', patterns)
        self.assertIn('app2:app2_view2', patterns)
        self.assertIn('app2:app2_view3', patterns)
        
        self.assertIn('app2:app3:app3_view1', patterns)
        self.assertIn('app2:app3:app3_view2', patterns)
        self.assertIn('app2:app3:app3_view3', patterns)
        
        self.assertIn('test', patterns)
        
    def test_3_patterns(self):
        context = build_context(ALL_NAMES)
        patterns = context['patterns']
    
        self.assertEqual('/app1/view2/(?P<param1>.+)', patterns['app1_view2'])
        self.assertEqual('/app1/view3', patterns['app1:app1_view3'])
        
        self.assertEqual('/app2/view1/(?P<param1>.+)/(?P<param2>.+)', patterns['app2:app2_view1'])
        self.assertEqual('/app2/view2/(.+)/(.+)', patterns['app2:app2_view2'])
        self.assertEqual('/app2/view3/(.+)/(.+)/(?P<param1>.+)/(?P<param2>.+)', patterns['app2:app2_view3'])
        
        self.assertEqual('/app2/app3/(?P<param1>.+)/(?P<param2>.+)/view1/(?P<param3>.+)/(?P<param4>.+)', patterns['app2:app3:app3_view1'])
        self.assertEqual('/app2/app3/(?P<param1>.+)/(?P<param2>.+)/view2/(.+)/(.+)', patterns['app2:app3:app3_view2'])
        self.assertEqual('/app2/app3/(?P<param1>.+)/(?P<param2>.+)/view3/(?P<param3>.+)/(?P<param4>.+)/(.+)/(.+)', patterns['app2:app3:app3_view3'])
        
        self.assertEqual('/', patterns['test'])
        
    def test_4_no_view_context(self):
        self.assertRaises(NoReverseMatch, build_context, 'app1_view1') # not named view
        self.assertRaises(NoReverseMatch, build_context, 'app1:app1_view4') # not existing view
        
    def test_5_one_view_context(self):
        context = build_context('app1_view2')
        patterns = context['patterns']
        
        self.assertNotIn('app1_view1', patterns)
        self.assertIn('app1_view2', patterns)
        self.assertNotIn('app1:app1_view3', patterns)
        
        self.assertNotIn('app2:app2_view1', patterns)
        self.assertNotIn('app2:app2_view2', patterns)
        self.assertNotIn('app2:app2_view3', patterns)
        
        self.assertNotIn('app2:app3:app3_view1', patterns)
        self.assertNotIn('app2:app3:app3_view2', patterns)
        self.assertNotIn('app2:app3:app3_view3', patterns)
        
        self.assertNotIn('test', patterns)
        
    def test_6_two_view_context(self):
        context = build_context('app1_view2', 'app2:app2_view1')
        patterns = context['patterns']
        
        self.assertNotIn('app1_view1', patterns)
        self.assertIn('app1_view2', patterns)
        self.assertNotIn('app1:app1_view3', patterns)
        
        self.assertIn('app2:app2_view1', patterns)
        self.assertNotIn('app2:app2_view2', patterns)
        self.assertNotIn('app2:app2_view3', patterns)
        
        self.assertNotIn('app2:app3:app3_view1', patterns)
        self.assertNotIn('app2:app3:app3_view2', patterns)
        self.assertNotIn('app2:app3:app3_view3', patterns)
        
        self.assertNotIn('test', patterns)
        
    def test_7_wildcard_outer_namespace_context(self):
        context = build_context('app2:' + ALL_NAMES)
        patterns = context['patterns']
        
        self.assertNotIn('app1_view1', patterns)
        self.assertNotIn('app1_view2', patterns)
        self.assertNotIn('app1:app1_view3', patterns)
        
        self.assertIn('app2:app2_view1', patterns)
        self.assertIn('app2:app2_view2', patterns)
        self.assertIn('app2:app2_view3', patterns)
        
        self.assertIn('app2:app3:app3_view1', patterns)
        self.assertIn('app2:app3:app3_view2', patterns)
        self.assertIn('app2:app3:app3_view3', patterns)
        
    def test_8_wildcard_inner_namespace_context(self):
        context = build_context('app2:app3:' + ALL_NAMES)
        patterns = context['patterns']
        
        self.assertNotIn('app1_view1', patterns)
        self.assertNotIn('app1_view2', patterns)
        self.assertNotIn('app1:app1_view3', patterns)
        
        self.assertNotIn('app2:app2_view1', patterns)
        self.assertNotIn('app2:app2_view2', patterns)
        self.assertNotIn('app2:app2_view3', patterns)
        
        self.assertIn('app2:app3:app3_view1', patterns)
        self.assertIn('app2:app3:app3_view2', patterns)
        self.assertIn('app2:app3:app3_view3', patterns)
        
        self.assertNotIn('test', patterns)
        
    def test_9_mixed_single_and_wildcard_context(self):
        context = build_context('app1_view2', 'app2:app3:' + ALL_NAMES)
        patterns = context['patterns']
        
        self.assertNotIn('app1_view1', patterns)
        self.assertIn('app1_view2', patterns)
        self.assertNotIn('app1:app1_view3', patterns)
        
        self.assertNotIn('app2:app2_view1', patterns)
        self.assertNotIn('app2:app2_view2', patterns)
        self.assertNotIn('app2:app2_view3', patterns)
        
        self.assertIn('app2:app3:app3_view1', patterns)
        self.assertIn('app2:app3:app3_view2', patterns)
        self.assertIn('app2:app3:app3_view3', patterns)
        
        self.assertNotIn('test', patterns)