using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace TrafficAnalyzerUI
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
            dateTimePicker1.Hide();
            label2.Hide();
        }

        private void comboBox1_SelectedIndexChanged(object sender, EventArgs e)
        {
            Console.WriteLine(e);
        }
        void comboBox1_DropDownClosed(object sender, EventArgs e)
        {
            this.BeginInvoke(new Action(() => { comboBox1.Select(0, 0); }));
        }
        private void label1_Click(object sender, EventArgs e)
        {

        }

        private void label2_Click(object sender, EventArgs e)
        {

        }

        private void dateTimePicker1_ValueChanged(object sender, EventArgs e)
        {

        }

        private void radioButton1_CheckedChanged(object sender, EventArgs e)
        {
            dateTimePicker1.Hide();
            label2.Hide();
        }

        private void radioButton2_CheckedChanged(object sender, EventArgs e)
        {
            dateTimePicker1.Show();
            label2.Show();
        }

        private void panel1_Paint(object sender, PaintEventArgs e)
        {

        }

        private void label3_Click(object sender, EventArgs e)
        {

        }

        private void panel1_Paint_1(object sender, PaintEventArgs e)
        {

        }
        public Image Base64ToImage(string base64String)
        {
            // Convert base 64 string to byte[]
            byte[] imageBytes = Convert.FromBase64String(base64String);
            // Convert byte[] to Image
            using (var ms = new MemoryStream(imageBytes, 0, imageBytes.Length))
            {
                Image image = Image.FromStream(ms, true);
                return image;
            }
        }
        private void button1_Click(object sender, EventArgs e)
        {
            try
            {

                // string x = RunPython.run_cmd("", "G:\\test.py");
                string code_path = AppDomain.CurrentDomain.BaseDirectory;
                // labelpy.Text = x;
                if (radioButton1.Checked)
                {
                    var area = comboBox1.SelectedItem.ToString();
                    var dateTime = DateTime.Now;
                    var day = dateTime.DayOfWeek.ToString();
                    var timeOnly = dateTime.ToString("HH:mm");
                    string x = RunPython.run_cmd("", $@"{code_path}Codes\analyze.py {area} {day} {timeOnly}");
                    panel3.BackgroundImage = Base64ToImage(x);
                }
                else
                {
                    var area = comboBox1.SelectedItem.ToString();
                    var dateTime = dateTimePicker1.Value;
                    var day = dateTime.DayOfWeek.ToString();
                    var timeOnly = dateTime.ToString("HH:mm");
                    string x = RunPython.run_cmd("", $@"{code_path}Codes\test.py {area} {day} {timeOnly}");
                    panel3.BackgroundImage = Base64ToImage(x);
                }
            }
            catch (Exception ex)
            {

                throw new Exception(ex.Message);
            }
            
        }

        private void button2_Click(object sender, EventArgs e)
        {
            if (radioButton1.Checked)
            {
                dateTimePicker1.Hide();
                label2.Hide();
            }
            labelpy.Hide();
            
        }

        private void panel3_Paint(object sender, PaintEventArgs e)
        {

        }
    }
}
