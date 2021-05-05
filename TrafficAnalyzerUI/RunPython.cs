using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace TrafficAnalyzerUI
{
    public class RunPython
    {
        public static string run_cmd(string cmd, string args)
        {
            Console.WriteLine(args);
            // args = "@" + string.Format("\"{0}\"", args);
            // Console.WriteLine(args);
            ProcessStartInfo start = new ProcessStartInfo();
            start.FileName = "C:\\Program Files (x86)\\Microsoft Visual Studio\\Shared\\Python37_64\\python.exe";
            start.Arguments = string.Format("{0} {1}", cmd, args);
            start.UseShellExecute = false;
            start.RedirectStandardOutput = true;
            string result;
            using (Process process = Process.Start(start))
            {
                using (StreamReader reader = process.StandardOutput)
                {
                    result = reader.ReadToEnd();
                    return result;
                }
            }
        }
    }
}
