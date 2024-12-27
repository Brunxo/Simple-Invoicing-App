import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from fpdf import FPDF

class InvoiceApp:
    def __init__(self, master):
        self.master = master
        master.title("Creador de Facturas Completo (Tabla Alineada)")

        # ---------- VARIABLES ----------
        self.items = []
        self.tax_rate = tk.DoubleVar(value=21.0)   # IVA por defecto 21%
        self.irpf_rate = tk.DoubleVar(value=15.0)  # IRPF por defecto 15%
        self.account_number = "ESXXXXXXXXXXXXXXXXXX"

        # ---------- SECCIÓN: DATOS DEL PROFESIONAL ----------
        self._create_professional_section()

        # ---------- SECCIÓN: DATOS DEL CLIENTE ----------
        self._create_client_section()

        # ---------- SECCIÓN: FACTURA (NÚMERO Y FECHA) ----------
        self._create_invoice_info_section()

        # ---------- SECCIÓN: ARTÍCULOS (CONCEPTOS) ----------
        self._create_items_section()

        # ---------- TABLA DE ITEMS ----------
        self._create_items_table()

        # ---------- IMPUESTOS ----------
        self._create_taxes_section()

        # ---------- BOTONES PDF ----------
        self._create_pdf_button()

        # Ajustar tamaño de columnas al redimensionar
        self.master.grid_columnconfigure((0,1,2,3), weight=1)
        self.master.grid_rowconfigure(10, weight=1)

    def _create_professional_section(self):
        prof_label = tk.Label(self.master, text="DATOS DEL PROFESIONAL", font=("Arial", 14, "bold"))
        prof_label.grid(row=0, column=0, columnspan=2, pady=(10, 5))

        tk.Label(self.master, text="Nombre:").grid(row=1, column=0, sticky="e")
        self.prof_name_entry = tk.Entry(self.master)
        self.prof_name_entry.grid(row=1, column=1, padx=5, pady=2)

        tk.Label(self.master, text="CIF/NIF:").grid(row=2, column=0, sticky="e")
        self.prof_cif_entry = tk.Entry(self.master)
        self.prof_cif_entry.grid(row=2, column=1, padx=5, pady=2)

        tk.Label(self.master, text="Dirección:").grid(row=3, column=0, sticky="e")
        self.prof_address_entry = tk.Entry(self.master)
        self.prof_address_entry.grid(row=3, column=1, padx=5, pady=2)

        tk.Label(self.master, text="Ciudad y CP:").grid(row=4, column=0, sticky="e")
        self.prof_city_entry = tk.Entry(self.master)
        self.prof_city_entry.grid(row=4, column=1, padx=5, pady=2)

        tk.Label(self.master, text="Teléfono:").grid(row=5, column=0, sticky="e")
        self.prof_phone_entry = tk.Entry(self.master)
        self.prof_phone_entry.grid(row=5, column=1, padx=5, pady=2)

    def _create_client_section(self):
        client_label = tk.Label(self.master, text="DATOS DEL CLIENTE", font=("Arial", 14, "bold"))
        client_label.grid(row=0, column=2, columnspan=2, padx=(20, 0), pady=(10, 5))

        tk.Label(self.master, text="Nombre o Razón Social:").grid(row=1, column=2, sticky="e")
        self.client_name_entry = tk.Entry(self.master)
        self.client_name_entry.grid(row=1, column=3, padx=5, pady=2)

        tk.Label(self.master, text="CIF/NIF:").grid(row=2, column=2, sticky="e")
        self.client_cif_entry = tk.Entry(self.master)
        self.client_cif_entry.grid(row=2, column=3, padx=5, pady=2)

        tk.Label(self.master, text="Dirección:").grid(row=3, column=2, sticky="e")
        self.client_address_entry = tk.Entry(self.master)
        self.client_address_entry.grid(row=3, column=3, padx=5, pady=2)

        tk.Label(self.master, text="Ciudad y CP:").grid(row=4, column=2, sticky="e")
        self.client_city_entry = tk.Entry(self.master)
        self.client_city_entry.grid(row=4, column=3, padx=5, pady=2)

    def _create_invoice_info_section(self):
        tk.Label(self.master, text="Número de Factura:").grid(row=6, column=0, sticky="e")
        self.invoice_num_entry = tk.Entry(self.master)
        self.invoice_num_entry.insert(0, "D/00206/2024")
        self.invoice_num_entry.grid(row=6, column=1, padx=5, pady=2)

        tk.Label(self.master, text="Fecha de la Factura:").grid(row=6, column=2, sticky="e")
        self.invoice_date_entry = tk.Entry(self.master)
        self.invoice_date_entry.grid(row=6, column=3, padx=5, pady=2)

    def _create_items_section(self):
        tk.Label(self.master, text="Ref:").grid(row=7, column=0, sticky="e")
        self.item_ref_entry = tk.Entry(self.master)
        self.item_ref_entry.grid(row=7, column=1, padx=5, pady=2)

        tk.Label(self.master, text="Descripción:").grid(row=7, column=2, sticky="e")
        self.item_desc_entry = tk.Entry(self.master)
        self.item_desc_entry.grid(row=7, column=3, padx=5, pady=2)

        tk.Label(self.master, text="Clases:").grid(row=8, column=0, sticky="e")
        self.item_classes_entry = tk.Entry(self.master)
        self.item_classes_entry.grid(row=8, column=1, padx=5, pady=2)

        tk.Label(self.master, text="Precio:").grid(row=8, column=2, sticky="e")
        self.item_price_entry = tk.Entry(self.master)
        self.item_price_entry.grid(row=8, column=3, padx=5, pady=2)

        tk.Button(self.master, text="Añadir Concepto", command=self.add_item).grid(row=9, column=0, columnspan=4, pady=(5, 10))

    def _create_items_table(self):
        columns = ("ref", "desc", "clases", "price")
        self.items_tree = ttk.Treeview(self.master, columns=columns, show="headings", height=6)
        self.items_tree.grid(row=10, column=0, columnspan=4, padx=5, sticky="nsew")

        for col in columns:
            self.items_tree.heading(col, text=col.title())
            self.items_tree.column(col, width=100)

    def _create_taxes_section(self):
        tk.Label(self.master, text="IVA (%):").grid(row=11, column=0, sticky="e")
        self.tax_entry = tk.Entry(self.master, textvariable=self.tax_rate)
        self.tax_entry.grid(row=11, column=1, padx=5, pady=2)

        tk.Label(self.master, text="IRPF (%):").grid(row=11, column=2, sticky="e")
        self.irpf_entry = tk.Entry(self.master, textvariable=self.irpf_rate)
        self.irpf_entry.grid(row=11, column=3, padx=5, pady=2)

    def _create_pdf_button(self):
        tk.Button(self.master, text="Generar PDF", command=self.generate_pdf_with_design).grid(row=12, column=0, columnspan=4, padx=5, pady=15)

    def add_item(self):
        """Agrega un ítem a la lista y lo muestra en el Treeview."""
        ref = self.item_ref_entry.get().strip()
        desc = self.item_desc_entry.get().strip()
        clases = self.item_classes_entry.get().strip()
        price_str = self.item_price_entry.get().strip()

        if not ref or not desc or not price_str:
            messagebox.showerror("Error", "Por favor, rellena todos los campos del concepto.")
            return

        try:
            price = float(price_str)
        except ValueError:
            messagebox.showerror("Error", "El precio debe ser un valor numérico.")
            return

        self.items_tree.insert("", tk.END, values=(ref, desc, clases, f"{price:.2f}"))
        self.items.append({"ref": ref, "desc": desc, "clases": clases, "price": price})

        # Limpieza de campos
        self.item_ref_entry.delete(0, tk.END)
        self.item_desc_entry.delete(0, tk.END)
        self.item_classes_entry.delete(0, tk.END)
        self.item_price_entry.delete(0, tk.END)

    def generate_pdf_with_design(self):
        """Genera un PDF con la última columna de 'Conceptos' alineada con la tabla de Totales."""
        if not self.items:
            messagebox.showerror("Error", "No hay ítems agregados. Añade al menos un concepto antes de generar la factura.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="Guardar Factura"
        )
        if not file_path:
            return

        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Helvetica", '', 10)

            margin_left = 15
            line_height = 6
            pdf.set_left_margin(margin_left)

            # ---------------- ENCABEZADO ----------------
            pdf.set_xy(margin_left, 10)
            pdf.set_font("Helvetica", 'B', 12)
            pdf.cell(40, line_height, "FACTURA", ln=0)

            invoice_num = self.invoice_num_entry.get()
            invoice_date = self.invoice_date_entry.get()

            pdf.set_xy(140, 10)
            pdf.cell(60, line_height, invoice_num, align="R", ln=0)

            pdf.set_xy(140, 16)
            pdf.set_font("Helvetica", '', 10)
            pdf.cell(60, line_height, invoice_date, align="R", ln=0)

            pdf.set_xy(margin_left, 16)
            pdf.cell(30, line_height, "Fecha:", ln=0)
            pdf.ln(15)

            # ---------------- DATOS EMISOR ----------------
            pdf.set_font("Helvetica", 'B', 10)
            pdf.cell(90, line_height, self.prof_name_entry.get(), ln=1)

            pdf.set_font("Helvetica", '', 10)
            if self.prof_cif_entry.get():
                pdf.cell(90, line_height, f"CIF/NIF: {self.prof_cif_entry.get()}", ln=1)
            pdf.cell(90, line_height, self.prof_address_entry.get(), ln=1)
            pdf.cell(90, line_height, self.prof_city_entry.get(), ln=1)
            if self.prof_phone_entry.get():
                pdf.cell(90, line_height, f"Telf: {self.prof_phone_entry.get()}", ln=1)

            # ---------------- DATOS CLIENTE ----------------
            x_client = 110
            y_client = 35
            pdf.set_xy(x_client, y_client)
            pdf.set_font("Helvetica", 'B', 10)
            pdf.cell(60, line_height, self.client_name_entry.get(), ln=1)

            pdf.set_font("Helvetica", '', 10)
            if self.client_cif_entry.get():
                pdf.set_xy(x_client, pdf.get_y())
                pdf.cell(60, line_height, f"CIF/NIF: {self.client_cif_entry.get()}", ln=1)

            pdf.set_xy(x_client, pdf.get_y())
            pdf.cell(60, line_height, self.client_address_entry.get(), ln=1)

            pdf.set_xy(x_client, pdf.get_y())
            pdf.cell(60, line_height, self.client_city_entry.get(), ln=1)
            pdf.ln(5)

            # ---------------- TÍTULO CONCEPTOS ----------------
            pdf.set_font("Helvetica", 'B', 10)
            pdf.cell(0, line_height, "CONCEPTOS", ln=1)
            pdf.ln(2)

            # ---------------- TABLA CONCEPTOS ----------------
            # Última columna termina en x=140 => ancho total = 125 (140 - 15).
            # Se reparten en: Ref (15), Descripción (60), Clases (25), Precio (25).
            w_ref, w_desc, w_clases, w_price = 15, 60, 25, 25

            pdf.set_font("Helvetica", 'B', 9)
            pdf.cell(w_ref, line_height, "Ref.", border=1, align="C")
            pdf.cell(w_desc, line_height, "Descripción", border=1, align="C")
            pdf.cell(w_clases, line_height, "Clases", border=1, align="C")
            pdf.cell(w_price, line_height, "Precio", border=1, align="C")
            pdf.ln(line_height)

            pdf.set_font("Helvetica", '', 9)

            subtotal = 0.0
            for item in self.items:
                ref = item["ref"]
                desc = item["desc"]
                clases = item["clases"]
                price = item["price"]
                subtotal += price

                pdf.cell(w_ref, line_height, ref, border=1, align="C")
                pdf.cell(w_desc, line_height, desc, border=1, align="L")
                pdf.cell(w_clases, line_height, clases, border=1, align="C")
                pdf.cell(w_price, line_height, f"{price:,.2f} EUR", border=1, align="R")
                pdf.ln(line_height)

            # ---------------- TOTALES (IVA/IRPF) ----------------
            iva_percent = self.tax_rate.get()
            iva_amount = (subtotal * iva_percent) / 100.0
            irpf_percent = self.irpf_rate.get()
            irpf_amount = (subtotal * irpf_percent) / 100.0
            total = subtotal + iva_amount - irpf_amount

            pdf.ln(5)
            x_totals = 140
            y_totals = pdf.get_y() + 10
            pdf.set_xy(x_totals, y_totals)

            pdf.set_font("Helvetica", '', 10)
            pdf.cell(40, line_height, "Base Liquid.", border=1, align="L")
            pdf.cell(25, line_height, f"{subtotal:,.2f} EUR", border=1, align="R", ln=1)

            pdf.set_x(x_totals)
            pdf.cell(40, line_height, f"I.V.A. (+{iva_percent}%)", border=1, align="L")
            pdf.cell(25, line_height, f"{iva_amount:,.2f} EUR", border=1, align="R", ln=1)

            pdf.set_x(x_totals)
            pdf.cell(40, line_height, f"I.R.P.F. (-{irpf_percent}%)", border=1, align="L")
            pdf.cell(25, line_height, f"{irpf_amount:,.2f} EUR", border=1, align="R", ln=1)

            pdf.set_font("Helvetica", 'B', 10)
            pdf.set_x(x_totals)
            pdf.cell(40, line_height, "Total", border=1, align="L")
            pdf.cell(25, line_height, f"{total:,.2f} EUR", border=1, align="R", ln=1)

            # ---------------- FORMA DE PAGO ----------------
            pdf.ln(10)
            pdf.set_font("Helvetica", 'B', 10)
            pdf.cell(0, line_height, "FORMA DE PAGO", ln=1)
            pdf.set_font("Helvetica", '', 10)
            pdf.cell(0, line_height, "(Transferencia bancaria)", ln=1)
            pdf.cell(0, line_height, self.account_number, ln=1)

            pdf.output(file_path)
            messagebox.showinfo("Éxito", f"Factura guardada correctamente:\n{file_path}")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el PDF.\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = InvoiceApp(root)
    root.mainloop()
