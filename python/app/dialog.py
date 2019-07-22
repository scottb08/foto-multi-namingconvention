# Copyright (c) 2013 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

import sys
import os
import re
import shutil
import subprocess
from pprint import pprint, pformat

import sgtk
# # by importing QT from sgtk rather than directly, we ensure that
# # the code will be compatible with both PySide and PyQt.
from sgtk.platform.qt import QtCore, QtGui
from .ui.dialog import Ui_Form

# import the context_selector module from the qtwidgets framework
context_selector = sgtk.platform.import_framework("tk-framework-qtwidgets", "context_selector")

# import the context_selector module from the qtwidgets framework
overlay_widget = sgtk.platform.import_framework("tk-framework-qtwidgets", "overlay_widget")

# import the task_manager module from shotgunutils framework
task_manager = sgtk.platform.import_framework("tk-framework-shotgunutils", "task_manager")

# import the shotgun_globals module from shotgunutils framework
shotgun_globals = sgtk.platform.import_framework("tk-framework-shotgunutils", "shotgun_globals")


def show_dialog(app_instance):
    """
    Shows the main dialog window.
    """
    # in order to handle UIs seamlessly, each toolkit engine has methods for launching
    # different types of windows. By using these methods, your windows will be correctly
    # decorated and handled in a consistent fashion by the system.

    # we pass the dialog class to this method and leave the actual construction
    # to be carried out by toolkit.
    app_instance.engine.show_dialog("Naming Convention Tool", app_instance, AppDialog)


class AppDialog(QtGui.QWidget):
    """
    Main application dialog window
    """

    def __init__(self):
        """
        Constructor
        """
        # first, call the base class and let it do its thing.
        QtGui.QWidget.__init__(self)

        self.context = None
        self.template = None
        self.fields = None
        self.ctx = None

        # Logging
        self.log = sgtk.platform.get_logger(__name__)

        # now load in the UI that was created in the UI designer
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # most of the useful accessors are available through the Application class instance
        # it is often handy to keep a reference to this. You can get it via the following method:
        self._app = sgtk.platform.current_bundle()

        # Get Application definitions
        self.applications = self._app.get_setting("tk-engines")

        self.template_definitions = self._app.get_setting("template_definitions")

        self.custom_entity_name_remap = self._app.get_setting("custom_entity_name_remap")

        self.restrict_entity_types = self._app.get_setting("restrict_entity_types")
        if self.restrict_entity_types:
            self.log.info('restrict_entity_types to: {}'.format(', '.join(self.restrict_entity_types)))

        self.restrict_entity_types_by_link = self._app.get_setting("restrict_entity_types_by_link")

        if self.restrict_entity_types_by_link:
            if 'entity' not in self.restrict_entity_types_by_link or 'field' not in self.restrict_entity_types_by_link:
                raise ValueError('"entity" or "field" key not defined for restrict_entity_types_by_link')

            self.log.info('restrict_entity_types_by_link to entity: {}, field: {}'.format(self.restrict_entity_types_by_link['entity'],
                                                                                          self.restrict_entity_types_by_link['field']))

        if self.restrict_entity_types and self.restrict_entity_types_by_link:
            raise ValueError('Please use either restrict_entity_types_by_link OR restrict_entity_types, but not both.')

        # via the self._app handle we can for example access:
        # - The engine, via self._app.engine
        # - A Shotgun API instance, via self._app.shotgun
        # - A tk API instance, via self._app.tk

        # create a background task manager for each of our components to use
        self._task_manager = task_manager.BackgroundTaskManager(self)
        self._task_manager.start_processing()

        # register it with the globals module so that it can
        # use it to fetch data
        shotgun_globals.register_bg_task_manager(self._task_manager)

        self._context_widget = context_selector.ContextWidget(self)
        self._context_widget.set_up(self._task_manager)

        # Disable "Link" widget in context selector so end user have to use "Task" widget instead
        self._context_widget.ui.link_label.setEnabled(True)
        self._context_widget.ui.link_search.setEnabled(True)
        self._context_widget.ui.link_display.setEnabled(True)
        self._context_widget.ui.link_search_btn.setEnabled(True)

        self._context_widget.set_task_tooltip('Type in the name of the Asset or Shot you are working on')

        self._overlay_widget = overlay_widget.ShotgunOverlayWidget(self)

        # Specify what entries should show up in the list of links when using
        # the auto completer. In this case, we only show entity types that are
        # allowed for the PublishedFile.entity field. You can provide an
        # explicit list with the `restrict_entity_types()` method.

        if self.restrict_entity_types_by_link:
            self._context_widget.restrict_entity_types_by_link(self.restrict_entity_types_by_link['entity'],
                                                               self.restrict_entity_types_by_link['field'])

        if self.restrict_entity_types:
            self._context_widget.restrict_entity_types(self.restrict_entity_types)

        # You can set the tooltip for each sub widget for context selection.
        # This helps describe to the user why they're choosing a task or link.
        self._context_widget.set_task_tooltip(
            "<p>The task that the selected item will be associated with the Shotgun entity being acted upon.</p>")

        self._context_widget.set_link_tooltip(
            "<p>The link that the selected item will be associated with the Shotgun entity being acted upon.</p>")

        # connect the signal emitted by the selector widget when a context is
        # selected. The connected callable should accept a context object.
        # self._context_widget.context_changed.connect(self._on_item_context_change)

        self.ui.contentWidgetVerticalLayout.addWidget(self._context_widget)

        # you can set a context using the `set_context()` method. Here we set it
        # to the current bundle's context
        self._context_widget.set_context(sgtk.platform.current_bundle().context)
        self._context_widget.context_changed.connect(self.define_tk_context)
        # self._context_widget.context_changed.connect(self.updateUi)

        # Connections
        self.ui.appComboBox.currentIndexChanged.connect(self.update_ui)
        self.ui.tkTemplateComboBox.currentIndexChanged.connect(self.update_ui)

        func = lambda x=self.ui.fileNameLineEdit: self.copy_path_to_clipboard(x)
        self.ui.fileNameCopyButton.released.connect(func)

        func = lambda x=self.ui.dirPathLineEdit: self.copy_path_to_clipboard(x)
        self.ui.directoryPathCopyButton.released.connect(func)

        func = lambda x=self.ui.filePathLineEdit: self.copy_path_to_clipboard(x)
        self.ui.filePathCopyButton.released.connect(func)

        func = lambda x=self.ui.dirPathLineEdit: self.open_file_path(x)
        self.ui.directoryPathOpenButton.released.connect(func)

        func = lambda x=self.ui.filePathLineEdit: self.open_file_path(x)
        self.ui.filePathOpenButton.released.connect(func)

        func = lambda x=self.ui.filePathLineEdit: self.create_file_on_disk(x)
        self.ui.createFileButton.released.connect(func)

        func = lambda x=self.ui.filePathLineEdit: self.create_file_on_disk(x)
        self.ui.createDirectoryButton.released.connect(func)

        self.ui.copyFilePathOpenButton.released.connect(self.browse_file)
        self.ui.copyFileToFileButton.released.connect(self.copy_file_to_file_path)

        self.update_applications()

    def update_applications(self):
        self.ui.appComboBox.clear()

        self.ui.appComboBox.addItem(QtGui.QIcon(':/res/block.png'), 'Select Application')

        app_keys = self.applications.keys()
        app_keys.sort()

        for appKey in app_keys:
            self.ui.appComboBox.addItem(QtGui.QIcon(':/res/sg_logo.png'), appKey, self.applications[appKey])

        self.ui.appComboBox.currentIndexChanged.connect(self.update_tk_context)
        self.ui.appComboBox.currentIndexChanged.connect(self.update_tk_templates)

    def update_tk_templates(self):
        if not self.context:
            self.log.error('TK context is not defined, unable to update TK templates.')
            return

        tk = self._app.context.sgtk

        if not tk:
            self.log.error('Unable to get TK instance, unable to update TK templates.')
            return

        templates = tk.templates

        # Support non-engine template definitions. If None, then use engine key name instead. ie: Data > data > take_data
        app_name = str(self.ui.appComboBox.itemData(self.ui.appComboBox.currentIndex()))
        if app_name:
            app_name = app_name.lower().replace(' ', '').replace('tk-', '')
        else:
            app_name = self.ui.appComboBox.currentText().lower()

        entity_type = self.context.entity['type']

        # Remap entity name
        entity_type = self.custom_entity_name_remap.get(entity_type, entity_type).lower()

        regex = '%s_%s' % (entity_type, app_name)

        active_templates = {}

        for k, v in templates.iteritems():
            if re.search(regex, k):
                active_templates[k] = v

        self.ui.tkTemplateComboBox.clear()

        active_keys = active_templates.keys()
        active_keys.sort()

        self.ui.tkTemplateComboBox.addItem(QtGui.QIcon(':/res/block.png'), 'Select Template')

        for key in active_keys:
            key_title = key.replace(entity_type, '').replace('_', ' ').title()
            self.ui.tkTemplateComboBox.addItem(QtGui.QIcon(':/res/sg_logo.png'), key_title, active_templates[key])

        # Default to "work" template if available
        index = self.ui.tkTemplateComboBox.findText('Work', QtCore.Qt.MatchContains)
        if index > -1:
            self.ui.tkTemplateComboBox.setCurrentIndex(index)

        self.ui.tkTemplateComboBox.currentIndexChanged.connect(self.update_template_definition)

        self.update_template_definition()

    def update_template_definition(self):
        """
        Show template definition if a match
        :return: None
        """

        curr_templ = self.ui.tkTemplateComboBox.itemText(self.ui.tkTemplateComboBox.currentIndex())
        self.ui.descriptionLabel.setText('')

        for k, v in self.template_definitions.iteritems():
            if re.search(k, curr_templ, re.IGNORECASE):
                self.ui.descriptionLabel.setText(v)

    def define_tk_context(self, context):
        if not context.task:
            return

        self.ui.appComboBox.setCurrentIndex(0)
        self.ui.tkTemplateComboBox.setCurrentIndex(0)
        self.clear_extra_token_widgets()

        self.context = context
        self.log.info('Context, source: %s' % self.context.source_entity)
        self.log.info('Context, task: %s' % self.context.task)

        self.update_ui()

    def update_tk_context(self):
        """
        Register selected context with Toolkit
        :return:
        """

        if self.ui.appComboBox.currentIndex() == 0:
            return

        tkengine = self.ui.appComboBox.itemData(self.ui.appComboBox.currentIndex())

        # Try to get as deep into valid context
        if self.context.task:
            typ = self.context.task['type']
            idd = self.context.task['id']

        elif self.context.step:
            typ = self.context.step['type']
            idd = self.context.step['id']

        elif self.context.source_entity:
            typ = self.context.source_entity['type']
            idd = self.context.source_entity['id']

        try:
            self._overlay_widget.show_message('<h2 style="color:#4383a8">Registering context with Toolkit, please wait...</h2>')
            QtGui.QApplication.instance().processEvents()
            self.log.info('Creating folder structure on disk')
            self._app.sgtk.create_filesystem_structure(typ, idd, engine=tkengine)

        except:
            pass

        finally:
            self._overlay_widget.hide()

        self.ctx = self._app.sgtk.context_from_entity(typ, idd)

    def update_template_output_paths(self):
        if self.ui.tkTemplateComboBox.currentIndex() == 0:
            return

        self.template = self.ui.tkTemplateComboBox.itemData(self.ui.tkTemplateComboBox.currentIndex())

        if not self.template:
            return

        # Update template definition label
        self.ui.tkTemplateComboBox.setToolTip(self.template.definition)

        self.fields = self.ctx.as_template_fields(self.template)

        missing_keys = self.template.missing_keys(self.fields)

        self.update_extra_tokens_widgets(self.template, missing_keys)

    def update_extra_tokens_widgets(self, template, missing_keys):
        missing_keys_dict = {}

        for key in missing_keys:
            if key in template.keys:
                keyObj = template.keys[key]
                missing_keys_dict[key] = keyObj

        parent = self.ui.extraTokensWidget
        parent_lay = self.ui.extraTokensWidgetLayout

        self.clear_extra_token_widgets()

        keys = missing_keys_dict.keys()
        keys.sort()

        row_cnt = 0

        if not keys:
            label = QtGui.QLabel('No Extra Keys found...', parent=parent)
            parent_lay.addWidget(label, row_cnt, 0)

        else:
            for key in keys:
                label = QtGui.QLabel(str(key), parent=parent)
                lineedit = QtGui.QLineEdit(str(missing_keys_dict[key].default), parent=parent)
                lineedit.data = missing_keys_dict[key]   # Not ideal to store to object, but QLabel has no data storage method

                lineedit.editingFinished.connect(self.update_template_file_path)

                parent_lay.addWidget(label, row_cnt, 0)
                parent_lay.addWidget(lineedit, row_cnt, 1)

                row_cnt += 1

    def get_extra_token_definitions(self):
        """
        Loop through all child qlabels gathering user input values
        :return:
        """
        parent = self.ui.extraTokensWidget

        missing_keys = {}
        valid = True

        for widget in parent.children():
            if type(widget) == QtGui.QLineEdit:

                value = widget.text()

                if not value:
                    widget.setStyleSheet('border: 1px solid red; border-radius: 6px;')
                    valid = False
                else:
                    widget.setStyleSheet('')

                    if type(widget.data) == sgtk.templatekey.IntegerKey:
                        missing_keys[widget.data.name] = int(value)

                    elif type(widget.data) == sgtk.templatekey.StringKey:
                        missing_keys[widget.data.name] = value

        return missing_keys, valid

    def clear_extra_token_widgets(self):
        parent = self.ui.extraTokensWidget

        # Delete child widgets of parent
        for widget in parent.children():
            if type(widget) == QtGui.QGridLayout:
                continue
            widget.deleteLater()

    def update_ui(self):
        # Disable widgets from user input
        self.ui.filePathWidgetGroup.setEnabled(False)
        self.ui.appComboBox.setEnabled(False)
        self.ui.tkTemplateComboBox.setEnabled(False)
        self.ui.fileNameLineEdit.setText('')
        self.ui.dirPathLineEdit.setText('')
        self.ui.filePathLineEdit.setText('')
        self.ui.copyFileLineEdit.setText('')

        if self.context:
            # Application combobox
            self.ui.appComboBox.setEnabled(True)
            if self.ui.appComboBox.currentIndex() < 1:
                self.ui.appComboBox.setStyleSheet('border: 1px solid blue; border-radius: 6px;')
                return
            else:
                self.ui.appComboBox.setStyleSheet('')

            # Template combobox
            self.clear_extra_token_widgets()
            self.ui.tkTemplateComboBox.setEnabled(True)
            if self.ui.tkTemplateComboBox.currentIndex() < 1:
                self.ui.tkTemplateComboBox.setStyleSheet('border: 1px solid blue; border-radius: 6px;')
                return
            else:
                self.ui.tkTemplateComboBox.setStyleSheet('')

            self.update_template_output_paths()

            self.update_template_file_path()

    def update_template_file_path(self):
        missing_keys, valid = self.get_extra_token_definitions()

        # Invalid state means that not all extra tokens are valid or missing
        if not valid:
            self.ui.filePathWidgetGroup.setEnabled(False)
            return

        self.ui.filePathWidgetGroup.setEnabled(True)

        self.fields.update(missing_keys)

        filepath = self.template.apply_fields(self.fields)

        # replace any frame padding with value
        try:
            filepath = filepath % 1

        except:
            pass

        if self.is_path_file(filepath):
            self.ui.fileNameLineEdit.setText(os.path.basename(filepath))
        else:
            self.ui.fileNameLineEdit.setText('Template is a directory')

        self.ui.dirPathLineEdit.setText(os.path.dirname(filepath))
        self.ui.filePathLineEdit.setText(filepath)

    def sanitize_file_path(self, path):
        illegalchars = ['<', '>', '|', '*', '"', '?']

        for x in illegalchars:
            path = path.replace(x, '')

        return path

    def copy_path_to_clipboard(self, widget):
        """

        :param widget: Widget to get path from to copy to clipboard
        :return:
        """
        cb = QtGui.QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(self.sanitize_file_path(widget.text()), mode=cb.Clipboard)

    def open_file_path(self, widget):

        path = widget.text()
        path = self.sanitize_file_path(path)

        if os.path.isfile(path):
            path = os.path.dirname(path)

        while True:
            if os.path.exists(path):
                break
            path = os.path.dirname(path)

        if sys.platform == 'darwin':
            subprocess.call(["open", "-R", path])

        elif sys.platform == 'win32':
            os.startfile(path)

        elif sys.platform == 'linux2':
            subprocess.Popen(['xdg-open', path])

    def browse_file(self):
        file_name = QtGui.QFileDialog.getOpenFileName()
        self.ui.copyFileLineEdit.setText(file_name[0])

    def create_file_on_disk(self, widget):
        path = widget.text()
        path = self.sanitize_file_path(path)

        is_file = self.is_path_file(path)

        try:
            if not os.path.exists(path):

                if is_file:
                    dirpath = os.path.dirname(path)
                else:
                    dirpath = path

                # Create directory structure first
                if not os.path.exists(dirpath):
                    os.makedirs(dirpath)
                    self.log.info('Created directories: %s' % dirpath)

                if is_file:
                    file(path, 'w').close()
                    self.log.info('Created file: %s' % path)

            QtGui.QMessageBox.information(self, 'Success!',
                                          '<h3>Created directory/file:</h3><br>{}</br>'.format(path),
                                          QtGui.QMessageBox.Ok)

        except Exception as err:
            QtGui.QMessageBox.critical(self, 'Failure!',
                                       '<h3>The directory/file failed to be created: {}</h3><br>{}</br>'.format(path,
                                                                                                                str(err)),
                                       QtGui.QMessageBox.Ok)
            self.log.error('Failed to create directory/file: {}'.format(path))
            self.log.error(str(err))

    @staticmethod
    def is_path_file(path):
        """
        Check if the path has a file extension, assume its a file, if not its a directory
        :param path: str - directory/file path
        :return: bool
        """
        tmp = os.path.splitext(path)
        if len(tmp) > 1 and tmp[1]:
            return True

        return False

    def copy_file_to_file_path(self):
        src_path = self.ui.copyFileLineEdit.text()
        dst_path = self.ui.filePathLineEdit.text()

        if not os.path.exists(src_path):
            self.log.warn('File doesnt not exist on disk, unable to copy: %s' % src_path)
            return

        # Check if file exists
        if os.path.exists(dst_path):
            reply = QtGui.QMessageBox.question(self, 'File Exists',
                                               'The file already exists, do you want to overwrite it?',
                                               QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)

            if reply == QtGui.QMessageBox.Yes:
                try:
                    os.remove(dst_path)
                    self.log.info('Removed existing file: {}'.format(dst_path))
                except Exception as err:
                    self.log.error('Failed to remove existing file: %s'.format(dst_path))
                    self.log.error(str(err))
            else:
                return

        # Copy file
        try:
            self.log.info('Copying: {} > {}'.format(src_path, dst_path))

            dirname = os.path.dirname(dst_path)
            if not os.path.exists(dirname):
                os.makedirs(dirname)

            shutil.copyfile(src_path, dst_path)

            QtGui.QMessageBox.information(self, 'Success!',
                                          '<h3>The file was copied successfully</h3>',
                                          QtGui.QMessageBox.Ok)

            self.ui.copyFileLineEdit.clear()

        except Exception as err:
            QtGui.QMessageBox.critical(self, 'Failure!',
                                       '<h3>The file failed to be copied</h3><br>{}</br>'.format(str(err)),
                                       QtGui.QMessageBox.Ok)
            self.log.error('Failed to copy: {} > {}'.format(src_path, dst_path))
            self.log.error(str(err))

    def closeEvent(self, event):
        """
        Executed when the main dialog is closed.
        All worker threads and other things which need a proper shutdown
        need to be called here.
        """

        self.log.debug("CloseEvent Received. Begin shutting down UI.")

        # register the data fetcher with the global schema manager
        shotgun_globals.unregister_bg_task_manager(self._task_manager)

        try:
            # shut down main threadpool
            self._task_manager.shut_down()
        except Exception:
            self.log.exception("Error running closeEvent()")

        # ensure the context widget's recent contexts are saved
        self._context_widget.save_recent_contexts()

    # def _on_item_context_change(self, context):
    #     """
    #     This method is connected above to the `context_changed` signal emitted
    #     by the context selector widget.
    #
    #     For demo purposes, we simply display the context in a label.
    #     """
    #     self._context_lbl.setText("Context set to: %s" % (context,))
    #
    #     # typically the context would be set by some external process. for now,
    #     # we'll just re-set the context based on what was selected. this will
    #     # have the added effect of populating the "recent" items in the drop
    #     # down list
    #     self._context_widget.set_context(context)

    # def _enable_editing(self, checked):
    #     """
    #     This method is connected above to the toggle button to show switching
    #     between enabling and disabling editing of the context.
    #     """
    #
    #     self._context_lbl.setText("")
    #
    #     if checked:
    #         # enable editing and show a message to the user
    #         self._context_widget.enable_editing(
    #             True,
    #             "Editing is now enabled."
    #         )
    #     else:
    #         # disable editing and show a message to the user
    #         self._context_widget.enable_editing(
    #             False,
    #             "Editing is now disabled."
    #         )
