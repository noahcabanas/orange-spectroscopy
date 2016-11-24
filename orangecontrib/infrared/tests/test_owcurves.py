import numpy as np
import Orange
from Orange.widgets.tests.base import WidgetTest
from orangecontrib.infrared.widgets.owcurves import OWCurves
from orangecontrib.infrared.data import getx
from orangecontrib.infrared.widgets.line_geometry import intersect_curves_chunked

class TestOWCurves(WidgetTest):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.iris = Orange.data.Table("iris")
        cls.collagen = Orange.data.Table("collagen")

    def setUp(self):
        self.widget = self.create_widget(OWCurves)

    def test_handle_floatname(self):
        self.send_signal("Data", self.collagen)
        curves = self.widget.plotview.curves
        self.assertEqual(len(curves), len(self.collagen))
        fs = sorted([float(f.name) for f in self.collagen.domain.attributes])
        np.testing.assert_equal(curves[0][0], fs)

    def test_handle_nofloatname(self):
        self.send_signal("Data", self.iris)
        curves = self.widget.plotview.curves
        self.assertEqual(len(curves), len(self.iris))
        np.testing.assert_equal(curves[0][0],
                                range(len(self.iris.domain.attributes)))

    def test_show_average(self):
        # curves_plotted changed with view switching, curves does not
        self.send_signal("Data", self.iris)
        curves = self.widget.plotview.curves
        curves_plotted = self.widget.plotview.curves_plotted
        self.widget.plotview.show_average()
        curves2 = self.widget.plotview.curves
        self.assertIs(curves, curves2)
        curves_plotted2 = self.widget.plotview.curves_plotted
        self.assertLess(len(curves_plotted2), len(curves_plotted))
        self.widget.plotview.show_individual()
        curves_plotted3 = self.widget.plotview.curves_plotted
        self.assertEqual(curves_plotted, curves_plotted3)

    def test_line_intersection(self):
        data = self.collagen
        x = getx(data)
        sort = np.argsort(x)
        x = x[sort]
        ys = data.X[:, sort]
        boola = intersect_curves_chunked(x, ys, np.array([0, 1.15]), np.array([3000, 1.15]))
        intc = np.flatnonzero(boola)
        np.testing.assert_equal(intc, [191, 635, 638, 650, 712, 716, 717, 726])