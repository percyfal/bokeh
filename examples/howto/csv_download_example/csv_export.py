import bokeh
import pandas as pd

from bokeh.plotting import ColumnDataSource
from bokeh.models import CustomJS, HBox, VBox, VBoxForm
from bokeh.models.widgets import Slider, Button, DataTable, TableColumn
from bokeh.io import curdoc, vform

# note this is fake data
df = pd.read_csv('salary_data.csv')

salary_range = Slider(title="Max Salary", start=10000, end=250000, value=150000, step=1000)
button = Button(label="Download", type="success")

source = ColumnDataSource(data=df)

columns = [TableColumn(field="name", title="Employee Name"),
           TableColumn(field="salary", title="Income"),
           TableColumn(field="years_experience", title="Experience (years)")]

data_table = DataTable(source=source, columns=columns)

def update(attr, old, new):
    curr_df = df[df['salary'] <= salary_range.value].dropna()
    source.data = dict(name=curr_df['name'].tolist(),
                       salary=curr_df['salary'].tolist(),
                       years_experience=curr_df['years_experience'].tolist())


salary_range.on_change('value', update)

js_callback = """
var csv = source.get('data');
var filetext = 'name,income,years_experience\\n';
for (i=0; i < csv['name'].length; i++) {
    var currRow = [csv['name'][i].toString(),
                   csv['salary'][i].toString(),
                   csv['years_experience'][i].toString().concat('\\n')];

    var joined = currRow.join();
    filetext = filetext.concat(joined);
}

var filename = 'data_result.csv';
var blob = new Blob([filetext], { type: 'text/csv;charset=utf-8;' });

if (navigator.msSaveBlob) {
navigator.msSaveBlob(blob, filename);
} else {
var link = document.createElement("a");
if (link.download !== undefined) {
    var url = URL.createObjectURL(blob);
    link.setAttribute("href", url);
    link.setAttribute("download", filename);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}
}"""

button.callback = CustomJS(args=dict(source=source), code=js_callback)
controls = [salary_range, button]
inputs = HBox(VBoxForm(*controls), width=400)
update(None, None, None)
curdoc().add_root(HBox(inputs, data_table, width=800))
