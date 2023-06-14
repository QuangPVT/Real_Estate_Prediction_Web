using System.ComponentModel.Design;

namespace Manage_Teacher_Information
{
    internal class Program
    {
        static void Main(string[] args)
        {
            // khai bao bien, mang va doi tuong
            var UI = new UI();
            GiaoVien[] list_gv = null;
            GiaoVien gv = new GiaoVien();
            int n = 0;
            int chucnang = 0;
            bool status = true;
            string input;

            // Bat dau Menu

            while (status)
            {
                UI.Menu(n);
                while (true)
                {
                    input = Console.ReadLine();
                    if (input.All(char.IsDigit))
                    {
                        chucnang = int.Parse(input);
                        break;
                    }
                    Console.WriteLine("Dau vao khong hop le!!!");
                    Console.WriteLine("Vui long nhap lai: ");
                }
                
                switch (chucnang)
                {
                    case 1:
                        n = UI.ChucNang_1();
                        break;

                    case 2:
                        if (n > 0)
                            list_gv = UI.ChucNang_2(n);
                        else
                            Console.WriteLine("Chua nhap so luong giao vien!!!");
                        Console.WriteLine("Nhan phim bat ki de tiep tuc...");
                        Console.ReadKey();
                        break;

                    case 3:
                        if (list_gv != null && n > 0)
                        {
                            UI.ChucNang_3(list_gv, n);
                        }
                        else
                        {
                            Console.WriteLine("Chua nhap du lieu dau vao!!!");
                        }
                        Console.WriteLine("Nhan phim bat ki de tiep tuc...");
                        Console.ReadKey();
                        break;

                    case 4:
                        if (list_gv != null && n > 0)
                        {
                            UI.ChucNang_4_LuaChon(list_gv, n);
                        }
                        else
                        {
                            Console.WriteLine("Chua nhap du lieu dau vao!!!");
                        }
                        Console.WriteLine("Nhan phim bat ki de tiep tuc...");
                        Console.ReadKey();
                        break;

                    case 0:
                        status = false;
                        break;
                }
            }
        }
    }
}