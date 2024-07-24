














def checkbox_linked_test(self, widget, checkbox_name, setting_name):
    def _get_checkbox():
        return getattr(widget.controls, checkbox_name)

    def get_checkbox():
        checkbox = _get_checkbox()
        return checkbox.isChecked()
    
    def set_checkbox(flag):
        checkbox = _get_checkbox()
        checkbox.setChecked(flag)
    
    def get_setting():
        return getattr(widget, setting_name)
    
    def set_setting(flag):
        setattr(widget, setting_name, flag)


    default_setting = get_setting()
    default_checkbox = get_checkbox()

    # Setting and checkbox checked should be the same.
    self.assertEqual(
        default_setting,
        default_checkbox,
        "setting and checkbox checked don't have the same initial value"
    )

    # Changing checkbox checked should change the setting.
    set_checkbox(not default_setting)

    self.assertEqual(
        get_checkbox(),
        not default_setting,
        "'checkbox.setChecked(flag)' didn't check checkbox"
    )

    self.assertEqual(
        get_setting(),
        not default_setting,
        "setting didn't change when checkbox checked did"
    )

    # Changing the setting should change checkbox checked.
    set_setting(default_setting)

    self.assertEqual(
        get_setting(),
        default_setting,
        "'setting=flag' didn't change setting to flag"
    )

    self.assertEqual(
        get_checkbox(),
        default_setting,
        "checkbox checked didn't change when setting did"
    )
