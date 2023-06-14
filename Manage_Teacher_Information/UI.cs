using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Manage_Teacher_Information
{
    public class UI
    {
        public string input;

        public void Menu(int n)
        {
            Console.Clear();
            Console.WriteLine("-----( Ung dung quan ly thong tin giao vien )-----");
            Console.WriteLine("===================( Thong tin )==================");
            Console.WriteLine("         So luong giao vien hien tai la: " + n);
            Console.WriteLine("================( MENU chuc nang )================");
            Console.WriteLine("     [1] Nhap so luong giao vien muon quan ly");
            Console.WriteLine("     [2] Them du lieu cho tat ca giao vien");
            Console.WriteLine("     [3] Tang he so luong cho giao vien");
            Console.WriteLine("     [4] Hien thi thong tin cua cac giao vien");
            Console.WriteLine("     [0] Thoat ung dung!");
            Console.WriteLine("==================================================");
            Console.WriteLine("- Moi ban lua chon chuc nang: ");
        }

        public int ChucNang_1()
        {
            int n = 0;
            while (n <= 0)
            {
                Console.Clear();
                Console.WriteLine("-----( Ung dung quan ly thong tin giao vien )-----");
                Console.WriteLine("==================( Chuc nang 1 )=================");
                Console.WriteLine("Moi ban nhap so luong giao vien: ");
                input = Console.ReadLine();
                if (input.All(char.IsDigit))
                    n = int.Parse(input);
                else
                {
                    Console.WriteLine("Dau vao khong hop le!!!");
                    Console.WriteLine("Nhan phim bat ki de tiep tuc...");
                    Console.ReadKey();
                }
            }
            return n;
        }

        public GiaoVien[] ChucNang_2(int n)
        {
            GiaoVien[] list_gv = new GiaoVien[n];
            Console.Clear();
            Console.WriteLine("-----( Ung dung quan ly thong tin giao vien )-----");
            Console.WriteLine("==================( Chuc nang 2 )=================");
            Console.WriteLine("Moi ban nhap du lieu tung giao vien:");
            for (int i = 0; i < n; i++)
            {
                GiaoVien gv = new GiaoVien();
                Console.WriteLine("STT: " + (i + 1));
                while (true)
                {
                    Console.Write("Ho va ten: ");
                    input = Console.ReadLine();
                    string temp = input.Replace(" ", "");
                    if (temp.All(Char.IsLetter))
                    {
                        gv.HoTen = input;
                        break;
                    }
                    Console.WriteLine("Dau vao khong hop le!!!");
                    Console.WriteLine("Vui long nhap lai!!! ");
                }
                
                while (true)
                {
                    Console.Write("Nam sinh: ");
                    input = Console.ReadLine();
                    if (input.All(Char.IsDigit))
                    {
                        gv.NamSinh = short.Parse(input);
                        break;
                    }
                    Console.WriteLine("Dau vao khong hop le!!!");
                    Console.WriteLine("Vui long nhap lai!!! ");
                }

                while (true)
                {
                    Console.Write("Luong co ban: ");
                    input = Console.ReadLine();
                    string temp = input.Replace(".", "");
                    if (temp.All(Char.IsDigit))
                    {
                        gv.LuongCoBan = double.Parse(input);
                        break;
                    }
                    Console.WriteLine("Dau vao khong hop le!!!");
                    Console.WriteLine("Vui long nhap lai!!! ");
                }

                while (true)
                {
                    Console.Write("He so luong: ");
                    input = Console.ReadLine();
                    string temp = input.Replace(".", "");
                    if (temp.All(Char.IsDigit))
                    {
                        gv.HeSoLuong =double.Parse(input);
                        break;
                    }
                    Console.WriteLine("Dau vao khong hop le!!!");
                    Console.WriteLine("Vui long nhap lai!!! ");
                }
                Console.Write("------");
                list_gv[i] = gv;
            }
            return list_gv;
        }

        public void ChucNang_3(GiaoVien[] list_gv, int n)
        {
            
            Console.Clear();
            Console.WriteLine("-----( Ung dung quan ly thong tin giao vien )-----");
            Console.WriteLine("==================( Chuc nang 3 )=================");

            int i = -1;
            while (i < 0 || i > n)
            {
                while (true)
                {
                    Console.WriteLine("Moi ban nhap ID cua giao vien trong danh sach:");
                    input = Console.ReadLine();
                    if (input.All(Char.IsDigit))
                    {
                        i = int.Parse(input);
                        break;
                    }
                    Console.WriteLine("Dau vao khong hop le!!!");
                    Console.WriteLine("Vui long nhap lai!!! ");
                }
                if (i < 0 || i > n)
                    Console.WriteLine("Khong co ID giao vien nay trong danh sach!");
            }

            Console.WriteLine("-------( Thong tin hien tai cua giao vien )-------");
            Console.WriteLine("ID: " + (i));
            Console.WriteLine("Ho va ten: " + list_gv[i-1].HoTen);
            Console.WriteLine("Nam sinh: " + list_gv[i-1].NamSinh);
            Console.WriteLine("Luong co ban: " + list_gv[i-1].LuongCoBan);
            Console.WriteLine("He so luong: " + list_gv[i-1].HeSoLuong);
            Console.WriteLine("----------( Thong tin sau khi thay doi )----------");
            Console.WriteLine("ID: " + (i));
            Console.WriteLine("Ho va ten: " + list_gv[i-1].HoTen);
            Console.WriteLine("Nam sinh: " + list_gv[i-1].NamSinh);
            Console.WriteLine("Luong co ban: " + list_gv[i-1].LuongCoBan);
            Console.WriteLine("He so luong: " + (list_gv[i-1].HeSoLuong + 0.6));
            Console.WriteLine("Ban co dong y thay doi nay? (Y/N): ");
            string key;
            while (true)
            {
                key = Console.ReadLine();

                if (key == "Y" || key == "y")
                {
                    Console.WriteLine("Da thay doi thanh cong!");
                    list_gv[i-1].XyLy();
                    break;
                }
                else if (key == "N" || key == "n")
                {
                    Console.WriteLine("Da huy thay doi!");
                    break;
                }
                else
                {
                    Console.WriteLine("Nhap sai ky tu! Moi nhap lai!");
                    Console.WriteLine("Ban co dong y thay doi nay? (Y/N): ");
                }
            }
        }

        public void ChucNang_4_Info(GiaoVien[] list_gv, int n)
        {
            Console.Clear();
            Console.WriteLine("-----( Ung dung quan ly thong tin giao vien )-----");
            Console.WriteLine("============( Chuc nang 4: Info only )============");
            for (int i = 0; i < n; i++)
            {
                Console.WriteLine("ID: " + (i + 1));
                Console.WriteLine("Ho va ten: " + list_gv[i].HoTen);
                Console.WriteLine("Nam sinh: " + list_gv[i].NamSinh);
                Console.WriteLine("Luong co ban: " + list_gv[i].LuongCoBan);
                Console.WriteLine("He so luong: " + list_gv[i].HeSoLuong);
                Console.WriteLine("Luong: " + list_gv[i].TinhLuong());
                Console.WriteLine("------");
            }
        }

        public void ChucNang_4_LuongASC(GiaoVien[] list_gv, int n)
        {
            GiaoVien[] temp_arr = list_gv;
            // Sap xep mang theo luong tang dan
            GiaoVien temp = new GiaoVien();
            for (int i = 0; i < n; i++)
            {
                for (int j = 0; j + 1 < n - i; j++)
                {
                    if (temp_arr[j].TinhLuong() > temp_arr[j + 1].TinhLuong())
                    {
                        temp = temp_arr[j];
                        temp_arr[j] = temp_arr[j + 1];
                        temp_arr[j + 1] = temp;
                    }
                }
            }

            // Hien thi thong tin
            Console.Clear();
            Console.WriteLine("-----( Ung dung quan ly thong tin giao vien )-----");
            Console.WriteLine("==========( Chuc nang 4: Luong tang dan )=========");
            for (int i = 0; i < n; i++)
            {
                Console.WriteLine("STT: " + (i + 1));
                Console.WriteLine("Ho va ten: " + temp_arr[i].HoTen);
                Console.WriteLine("Nam sinh: " + temp_arr[i].NamSinh);
                Console.WriteLine("Luong co ban: " + temp_arr[i].LuongCoBan);
                Console.WriteLine("He so luong: " + temp_arr[i].HeSoLuong);
                Console.WriteLine("Luong: " + temp_arr[i].TinhLuong());
                Console.WriteLine("------");
            }
        }

        public void ChucNang_4_LuongDES(GiaoVien[] list_gv, int n)
        {
            GiaoVien[] temp_arr = list_gv;
            // Sap xep mang theo luong giam dan
            GiaoVien temp = new GiaoVien();
            for (int i = 0; i < n; i++)
            {
                for (int j = 0; j + 1 < n - i; j++)
                {
                    if (temp_arr[j].TinhLuong() < temp_arr[j + 1].TinhLuong())
                    {
                        temp = temp_arr[j];
                        temp_arr[j] = temp_arr[j + 1];
                        temp_arr[j + 1] = temp;
                    }
                }
            }

            // Hien thi thong tin
            Console.Clear();
            Console.WriteLine("-----( Ung dung quan ly thong tin giao vien )-----");
            Console.WriteLine("=========( Chuc nang 4: Luong giam dan )==========");
            for (int i = 0; i < n; i++)
            {
                Console.WriteLine("STT: " + (i + 1));
                Console.WriteLine("Ho va ten: " + temp_arr[i].HoTen);
                Console.WriteLine("Nam sinh: " + temp_arr[i].NamSinh);
                Console.WriteLine("Luong co ban: " + temp_arr[i].LuongCoBan);
                Console.WriteLine("He so luong: " + temp_arr[i].HeSoLuong);
                Console.WriteLine("Luong: " + temp_arr[i].TinhLuong());
                Console.WriteLine("------");
            }
        }

        public void ChucNang_4_LuaChon(GiaoVien[] list_gv, int n)
        {
            Console.Clear();
            Console.WriteLine("-----( Ung dung quan ly thong tin giao vien )-----");
            Console.WriteLine("==================( Chuc nang 4 )=================");
            Console.WriteLine("         [1] Chi hien thong tin");
            Console.WriteLine("         [2] Sap xep theo luong tang dan");
            Console.WriteLine("         [3] Sap xep theo luong giam dan");
            Console.WriteLine("         [0] Quay lai menu chinh");
            Console.WriteLine("==================================================");
            
            int i = -1;
            while (i < 0 || i > 3)
            {
                while (true)
                {
                    Console.WriteLine("- Moi ban lua chon chuc nang: ");
                    input = Console.ReadLine();
                    if (input.All(Char.IsDigit))
                    {
                        i = int.Parse(input);
                        break;
                    }
                    Console.WriteLine("Dau vao khong hop le!!!");
                    Console.WriteLine("Vui long nhap lai!!! ");
                }

            }

            switch (i)
            {
                case 0:
                    break;

                case 1:
                    ChucNang_4_Info(list_gv, n);
                    break;

                case 2:
                    ChucNang_4_LuongASC(list_gv, n);
                    break;

                case 3:
                    ChucNang_4_LuongDES(list_gv, n);
                    break;
            }
        }
    }
}
