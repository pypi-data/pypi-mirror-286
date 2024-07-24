from typing import Dict, List, Union
from unittest import TestCase
from unittest.mock import patch

import django

django.setup()

from sens_platform.api.modules.types_modules.abc_type_modules import AbstractTypeModules


class FakeModule(AbstractTypeModules):
    """
    Fake class for tests.
    """

    _name: str = "Fake"

    def __init__(self, slug: str):
        super().__init__(slug)

    def execute(self) -> List[Dict]:
        pass

    def _to_dict(self, *args, **kwargs) -> Union[List[Dict], Dict]:
        pass

    def _generate_settings(self, *args, **kwargs) -> None:
        pass

    def _generate_data(self, *args, **kwargs) -> Union[List[Dict], Dict]:
        pass


class TestAbstractTypeModules(TestCase):
    def setUp(self) -> None:
        self.fake_slug = "site"
        self.concrete = FakeModule(self.fake_slug)

    def test_name_property(self) -> None:
        """Property validation."""
        self.assertIsNotNone(self.concrete.name)
        self.assertIsInstance(self.concrete.name, str)

    def test_slug(self) -> None:
        """Slug validation."""
        self.assertIsNotNone(self.concrete._slug)
        self.assertIsInstance(self.concrete._slug, str)
        self.assertEquals(self.concrete._slug, self.fake_slug)

    def test_execute_method(self):
        """Execution of function."""
        self.concrete.execute()

    def test_generate_settings_method(self):
        """Execution of function."""
        self.concrete._generate_settings()

    def test_to_dict_method(self):
        """Execution of function."""
        self.concrete._to_dict()

    def test_generate_data_method(self):
        """Execution of function."""
        self.concrete._generate_data()

    @patch.multiple(AbstractTypeModules, __abstractmethods__=set())
    def test_execute_abstract_method(self):
        """The return of raise is verified."""
        module = AbstractTypeModules(self.fake_slug)
        with self.assertRaises(NotImplementedError):
            module.execute()

    @patch.multiple(AbstractTypeModules, __abstractmethods__=set())
    def test_execute_abstract_method(self):
        """Validation of the returned error message."""
        module = AbstractTypeModules(self.fake_slug)
        try:
            module.execute()
        except NotImplementedError as e:
            self.assertEqual(str(e), "`execute` function not implemented.")

    @patch.multiple(AbstractTypeModules, __abstractmethods__=set())
    def test__generate_settings_abstract_method(self):
        """Validation of the returned error message."""
        module = AbstractTypeModules(self.fake_slug)
        try:
            module._generate_settings()
        except NotImplementedError as e:
            self.assertEqual(str(e), "`_generate_settings` function not implemented.")

    @patch.multiple(AbstractTypeModules, __abstractmethods__=set())
    def test__to_dict_abstract_method(self):
        """Validation of the returned error message."""
        module = AbstractTypeModules(self.fake_slug)
        try:
            module._to_dict()
        except NotImplementedError as e:
            self.assertEqual(str(e), "`_to_dict` function not implemented.")

    @patch.multiple(AbstractTypeModules, __abstractmethods__=set())
    def test__generate_data_abstract_method(self):
        """Validation of the returned error message."""
        module = AbstractTypeModules(self.fake_slug)
        try:
            module._generate_data()
        except NotImplementedError as e:
            self.assertEqual(str(e), "`_generate_data` function not implemented.")
