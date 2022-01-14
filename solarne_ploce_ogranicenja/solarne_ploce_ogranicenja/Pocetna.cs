using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace solarne_ploce_ogranicenja
{
    public partial class Pocetna : Form
    {
        string putDoSkripte = "";
        public Pocetna()
        {
            InitializeComponent();
        }

        private void izracunajAction_Click(object sender, EventArgs e)
        {
            if(float.TryParse(krov.Text, out _) && float.TryParse(cijena.Text, out _))
            {
                string argumenti = string.Format("{0} {1}", krov.Text, cijena.Text);
                int broj_ploca = Decimal.ToInt32(brojPloca.Value);
                for (int i = 1; i <= broj_ploca; i++)
                {
                    if(float.TryParse(Controls.Find("cijena"+i,true)[0].Text,out _) && float.TryParse(Controls.Find("watt" + i, true)[0].Text, out _) &&
                        float.TryParse(Controls.Find("velicina" + i, true)[0].Text, out _))
                    {
                        continue;
                    }
                    else
                    {
                        MessageBox.Show("Svi ulazi moraju biti brojevi");
                        return;
                    }
                }
                argumenti = dodaj_argumente(broj_ploca, argumenti, "naziv");
                argumenti = dodaj_argumente(broj_ploca, argumenti, "cijena");
                argumenti = dodaj_argumente(broj_ploca, argumenti, "watt");
                argumenti = dodaj_argumente(broj_ploca, argumenti, "velicina");
                pokreni_python_proces(argumenti);
            }
            else
            {
                MessageBox.Show("Cijena i velicina krova moraju biti brojevi!");
            }
        }

        private string dodaj_argumente(int br_ploca, string args, string izbor)
        {
            for(int i = 1; i <= br_ploca; i++)
            {
                if (izbor == "naziv")
                {
                    args = args + string.Format(" {0}", "tip_" + i);
                }
                if (izbor == "cijena")
                {
                    args = args + string.Format(" {0}", Controls.Find("cijena" + i, true)[0].Text);
                }
                if (izbor == "watt")
                {
                    args = args + string.Format(" {0}", Controls.Find("watt" + i, true)[0].Text);
                }
                if (izbor == "velicina")
                {
                    args = args + string.Format(" {0}", Controls.Find("velicina" + i, true)[0].Text);
                }
            }
            return args;
        }

        private void pokreni_python_proces(string args)
        {
            if(putDoSkripte == "")
            {
                MessageBox.Show("Molim učitajte skriptu.");
                return;
            }
            ProcessStartInfo start = new ProcessStartInfo();
            start.FileName = putDoSkripte;
            start.Arguments = args;
            start.UseShellExecute = false;
            start.RedirectStandardOutput = true;
            using (Process process = Process.Start(start))
            {
                using (StreamReader reader = process.StandardOutput)
                {
                    string result = reader.ReadToEnd();
                    IspisRezultata.Text = result;
                    IspisRezultata.Visible = true;

                }
            }
            Console.Read();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            OpenFileDialog ofd = new OpenFileDialog();
            ofd.Title = "Otvori python skriptu";
            ofd.Filter = "All Files(*.*)|*.*";
            DialogResult dr = ofd.ShowDialog();
            if (dr == DialogResult.OK)
            {
                string filePath = ofd.FileName;
                if (filePath.Length > 0)
                {
                    putDoSkripte = filePath;
                }
            }
        }
    }
}
