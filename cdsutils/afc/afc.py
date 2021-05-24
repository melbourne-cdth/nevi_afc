from IPython.display import HTML, display
import json
import sqlite3 as sq
import os
import shutil
import datetime
import markdown
import ipywidgets as ipw
import random
import gzip
from IPython.display import FileLink, FileLinks


try:
    username = os.environ["JUPYTERHUB_USER"]
except KeyError:
    username = 'unknown'

imgs=\
"""
<table>
   <tr>
      <td><img src="./media/ISIC_0000019.jpg" alt="a" width="256"></td>
      <td><img src="./media/ISIC_0000029.jpg" alt="b" width="256"></td>
      <td><img src="./media/ISIC_0000049.jpg" alt="c" width="256"></td>
      <td><img src="./media/ISIC_0000000.jpg" alt="d" width="256"></td>
    </tr>
   <tr>
      <td style="text-align:center">a</td><td style="text-align:center">b</td><td style="text-align:center">c</td><td style="text-align:center">d</td>
   </tr>
</table>
"""

class AFC4(ipw.VBox):
    
    _dname = "nevi_afc_responses.json.gz"

    def __init__(self):
        self.fname =os.path.join(".", "mydata.json.gz")
        self.dname = os.path.join(os.path.dirname(__file__), self._dname) 
        self.__mapping = {"a":"452914", "b":"452913", "c":"452915", "d":"452912"}
        with gzip.open(self.fname, "wt", encoding='utf-8') as f:
            json.dump({}, f)
                
        self.score = 0.0
        self.count = 0
        self.instructions = ipw.HTML("<h2>Select the image being described by the text</h2>")
        self.info = ipw.Label(value="")
        self.choices = ipw.Dropdown(options=['a', 'b', 'c', 'd'])
        self.submit = ipw.Button(description="submit")
        self.submit.on_click(self.on_submit)
        self.__imgs = ipw.HTML(imgs)
        self.__get_data()
        self._desc = ipw.HTML(markdown.markdown(self.__current_case[1]))
        self.__my_responses = {}

        self.num_remain = len(self._cases)
        super(AFC4, self).__init__(children=[self.instructions, self.info, self.__imgs, self._desc, self.choices, self.submit])
        
    def wrap_up(self):
         self.submit.layout.display = "none"
         self.choices.layout.display = "none"
         self.instructions.value = "<h3>Click on the link to download your results</h3>"
         self._desc.value = markdown.markdown("__After downloading the file, upload the file to Canvas to complete the assignment.__")
         display(FileLink(self.fname))

    def on_submit(self, *args):
            self.count += 1
            self.submit_answer()
            self.info.value = "%d cases completed; %d cases remaining"%(self.count, len(self._cases))

            try:
                self.__current_case = self._cases.pop()

                self._desc.value = markdown.markdown(self.__current_case[1])
                self.choices.value = 'a'
            except:
                self.wrap_up()
        
            
    def submit_answer(self):
        self.__my_responses[self.__current_case[0]] = self.choices.value
            
        with gzip.open(self.fname, "wt", encoding='utf-8') as f:
            json.dump(self.__my_responses, f)

        
    def __get_data(self):
        with gzip.open(self.dname, "rt", encoding='utf-8') as f:
            self._cases = json.load(f)
        random.shuffle(self._cases)
        self.__current_case = self._cases.pop()

