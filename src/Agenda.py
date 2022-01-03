import xlrd
from src.Event import Event

class Agenda:

  def __init__(self, sheetname):
    self.events = []
    self._parse_sheet(sheetname)


  def add_event(self, event):
    self.events.append(event)


  def __str__(self):
    return "\n".join(map(str, self.events))


  def _parse_sheet(self, filename):
    workbook = xlrd.open_workbook(filename)
    sh = workbook.sheet_by_index(0)
    row_dates = 4
    start_row_player = row_dates + 1 
    end_row_player = sh.nrows - 1 
    self._parse_dates(row_dates, sh)
    offset_dates = -1
    for i in range(start_row_player, end_row_player):
      player = sh.cell(i, 0).value
      for j in range(1, sh.ncols):
        value = sh.cell(i, j).value
        if value == "OK":
          self.events[j + offset_dates].add_player(player)

  def translate_month(self, date):
    month_dict = {
      "January": "Jan.", 
      "February": "Fév.", 
      "March": "Mars", 
      "April": "Avr.", 
      "May": "Mai", 
      "June": "Juin", 
      "July": "Juil.", 
      "August": "Août", 
      "September": "Sept.", 
      "October": "Oct.", 
      "November": "Nov.", 
      "December": "Déc."
    }
    res = date 
    for m in month_dict.keys():
      res = res.replace(m, month_dict[m])
    return res 


  def translate_day(self, date):
    day_dict = {
      "Mon": "Lun.", 
      "Tue": "Mar.", 
      "Wed": "Mer.", 
      "Thu": "Jeu.", 
      "Fri": "Ven.", 
      "Sat": "Sam.", 
      "Sun": "Dim."
    }
    res = date 
    for d in day_dict.keys():
      res = res.replace(d, day_dict[d])
    return res 


  def _parse_dates(self, row, sh):
    for j in range(1, sh.ncols):
      value = sh.cell(row-1, j).value
    current_month = self.translate_month(sh.cell(row-1, 1).value)
    for j in range(1, sh.ncols):
      if (v := sh.cell(row-1, j).value) != "":
        current_month = self.translate_month(v)
      value = self.translate_day(sh.cell(row, j).value)
      self.add_event(Event(value + " " + current_month))

