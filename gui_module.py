import tkinter as tk
import re

def click(place):
    print(place)


class MyApp:
    def __init__(self):
        self.window = tk.Tk()

        self.ent_place = self.set_frm_place()
        self.ent_check_in_date = self.set_frm_check_in_date()
        self.ent_check_out_date = self.set_frm_check_out_date()
        self.lbl_info = self.set_lbl_info()
        self.btn_search = self.set_btn_search()

        self.btn_search_is_clicked = False

    def set_frm_place(self):
        frm_place = tk.Frame(master=self.window)

        lbl_place = tk.Label(master=frm_place, text="Место/название объекта:")
        lbl_place.grid(row=0, column=0)

        ent_place = tk.Entry(master=frm_place, width=40)
        ent_place.grid(row=1, column=0)

        frm_place.grid(row=0, column=0, padx=5, pady=5)

        return ent_place

    def set_frm_check_in_date(self):
        frm_check_in_date = tk.Frame(master=self.window)

        lbl_check_in_date = tk.Label(master=frm_check_in_date, text="Дата заезда:")
        lbl_check_in_date.grid(row=0, column=0)

        ent_check_in_date = tk.Entry(master=frm_check_in_date, width=40)
        ent_check_in_date.grid(row=1, column=0)
        ent_check_in_date.insert(0, "31-07-2021")

        frm_check_in_date.grid(row=1, column=0, padx=5, pady=5)

        return ent_check_in_date

    def set_frm_check_out_date(self):
        frm_check_out_date = tk.Frame(master=self.window)

        lbl_check_out_date = tk.Label(master=frm_check_out_date, text="Дата отъезда:")
        lbl_check_out_date.grid(row=0, column=0)

        ent_check_out_date = tk.Entry(master=frm_check_out_date, width=40)
        ent_check_out_date.grid(row=1, column=0)
        ent_check_out_date.insert(0, "01-08-2021")

        frm_check_out_date.grid(row=2, column=0, padx=5, pady=5)

        return ent_check_out_date

    def set_btn_search(self):
        btn_search = tk.Button(text="Найти", width=20, height=1)
        btn_search.grid(row=4, column=0,  padx=5, pady=10)
        return btn_search

    def set_lbl_info(self):
        lbl_info = tk.Label(text="")
        lbl_info.grid(row=3, column=0)
        return lbl_info

    def onclick_btn_search(self):
        place = self.ent_place.get()
        check_in_date = self.ent_check_in_date.get()
        check_out_date = self.ent_check_out_date.get()
        print(place, check_in_date, check_out_date)
        self.btn_search_is_clicked = True

        # print(self.place, self.check_in_date, self.check_out_date)
        #
        # date_pattern = r"\d{2}-\d{2}-\d{4}"
        # if re.search(date_pattern, self.check_in_date):
        #     print("Yes")

    def mainloop(self):
        self.window.mainloop()

    def edit_lbl_info(self, new_text):
        self.lbl_info.configure(text=new_text)


if __name__ == '__main__':
    app = MyApp()
    app.mainloop()

