import pandas as pd # type:ignore
from Orange.data import Table
from Orange.data.pandas_compat import table_from_frame, table_to_frame
from Orange.widgets.widget import OWWidget, Input, Output
from Orange.widgets import gui
from AnyQt.QtWidgets import QListWidget, QListWidgetItem, QAbstractItemView

class OWSequenceChecker(OWWidget):
    name = "Sequence Checker"
    description = "Checks sequence of numbers"
    icon = "icons/sequence.svg"
    priority = 10
    
    class Inputs: # type: ignore
        data = Input("Data", Table)
        
    class Outputs: # type: ignore
        output_data = Output("Output Data", Table)
        
    want_main_area = False
    resizing_enabled = False
    
    def __init__(self):
        super().__init__()
        self.data = None
        
        # Control area
        box = gui.widgetBox(self.controlArea, "Settings")
        gui.label(box, self, "Sequence Checker Settings")
        
        # Column selection
        self.column_list = QListWidget()
        self.column_list.setSelectionMode(QAbstractItemView.SingleSelection)
        self.column_list.itemSelectionChanged.connect(self._on_column_changed)
        box.layout().addWidget(self.column_list)
        
        # Results
        self.result_label = gui.label(box, self, "No data processed yet.")
        
    @Inputs.data
    def set_data(self, data):
        """Set input data."""
        self.data = data
        if data is not None:
            df = table_to_frame(data)
            self.column_list.clear()
            for col in df.columns:
                item = QListWidgetItem(col)
                self.column_list.addItem(item)
            self.column_list.setCurrentRow(0)
            self.process_data()
            
    def _on_column_changed(self):
        if self.data is not None:
            self.process_data()
        
    def process_data(self):
        """Process the input data."""
        if self.data is None or not self.column_list.selectedItems():
            self.result_label.setText("No data processed yet.")
            return
        
        df = table_to_frame(self.data)
        selected_column = self.column_list.selectedItems()[0].text()
        
        if selected_column not in df.columns:
            self.result_label.setText("Selected column not in data.")
            return
        
        selected_series = df[selected_column]
        result = []
        anchor = selected_series.iloc[0]
        
        for i in selected_series:
            if anchor > i:
                tmp = (str(i) + ' Error Sequence')
            else:
                tmp = str(i)
            result.append(tmp)
            anchor = i
        
        doutput = {"SeqID": result}
        df_output = pd.DataFrame(doutput)
        out_data = table_from_frame(df_output)
        
        self.Outputs.output_data.send(out_data)
        self.result_label.setText(f"Processed {len(result)} rows.")

