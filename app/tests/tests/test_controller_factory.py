import pytest
from PyQt6.QtWidgets import QStackedWidget, QPushButton

from app.controllers.controller_factory import ControllerFactory, ControllerSection
from app.controllers.classes import ClassPart
from app.controllers.students import StudentsPart
from app.controllers.teacher import TeachersPart
from app.controllers.payment import PaymentPart
from app.controllers.others import SettingsLogic, UserPart


@pytest.fixture
def factory() -> ControllerFactory:
    return ControllerFactory()


class TestControllerSection:
    def test_all_sections_present(self):
        expected = {"students", "teachers", "classes", "finance",
                    "payments", "admin", "settings"}
        assert {s.value for s in ControllerSection} == expected


class TestControllerFactoryMapping:
    def test_mapping_contains_all_sections(self, factory: ControllerFactory):
        assert set(factory.controller.keys()) == set(ControllerSection)

    @pytest.mark.parametrize(
        "section,expected_cls",
        [
            (ControllerSection.STUDENTS, StudentsPart),
            (ControllerSection.TEACHERS, TeachersPart),
            (ControllerSection.CLASSES, ClassPart),
            (ControllerSection.PAYMENTS, PaymentPart),
            (ControllerSection.FINANCE, PaymentPart),
            (ControllerSection.ADMIN, UserPart),
            (ControllerSection.SETTINGS, SettingsLogic),
        ],
    )
    def test_section_maps_to_expected_class(self, factory: ControllerFactory, 
                                            section: ControllerSection, 
                                            expected_cls: type):
        assert factory.controller[section] is expected_cls

    def test_finance_and_payments_share_same_controller_class(self, factory: ControllerFactory):
        # FINANCE and PAYMENTS intentionally point to the same controller.
        assert factory.controller[ControllerSection.FINANCE] is \
            factory.controller[ControllerSection.PAYMENTS]


class TestCreateController:
    def test_create_controller_returns_instance_of_correct_class(self, qapp, factory: ControllerFactory):
        instance = factory.create_controller(ControllerSection.CLASSES)
        assert isinstance(instance, ClassPart)

    def test_create_controller_returns_new_instance_each_call(self, qapp, factory: ControllerFactory):
        first = factory.create_controller(ControllerSection.STUDENTS)
        second = factory.create_controller(ControllerSection.STUDENTS)
        assert first is not second

    def test_create_controller_raises_for_unknown_section(self, factory: ControllerFactory):
        with pytest.raises(ValueError, match="No controller found for section"):
            factory.create_controller("not_a_real_section")

    def test_create_controller_error_message_includes_section(self, factory: ControllerFactory):
        with pytest.raises(ValueError) as exc_info:
            factory.create_controller("bogus")
        assert "bogus" in str(exc_info.value)


class TestSetupSections:
    def test_setup_sections_adds_a_widget_per_section(self, qapp, factory: ControllerFactory):
        stacked_widget = QStackedWidget()
        buttons = {section: QPushButton() for section in ControllerSection}

        factory.setup_sections(stacked_widget, buttons)

        assert stacked_widget.count() == len(ControllerSection)

    def test_setup_sections_widgets_have_correct_types(self, qapp, factory: ControllerFactory):
        stacked_widget = QStackedWidget()
        buttons = {section: QPushButton() for section in ControllerSection}

        factory.setup_sections(stacked_widget, buttons)

        widget_types = {type(stacked_widget.widget(i)) for i in range(stacked_widget.count())}
        expected_types = set(factory.controller.values())
        assert widget_types == expected_types

    def test_setup_sections_raises_keyerror_if_button_missing(self, qapp, factory: ControllerFactory):
        stacked_widget = QStackedWidget()
        # Missing a button for one of the sections.
        incomplete_buttons = {
            section: QPushButton()
            for section in list(ControllerSection)[:-1]
        }
        with pytest.raises(KeyError):
            factory.setup_sections(stacked_widget, incomplete_buttons)


class TestSwitchSection:
    def test_switch_section_sets_current_widget(self, qapp, factory: ControllerFactory):
        stacked_widget = QStackedWidget()
        target = ClassPart()
        stacked_widget.addWidget(target)

        factory.switch_section(stacked_widget, target)

        assert stacked_widget.currentWidget() is target
