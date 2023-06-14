using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Manage_Teacher_Information
{
    public class NguoiLaoDong
    {
        // Thuoc tinh
        public string HoTen;
        public short NamSinh;
        public double LuongCoBan;

        // Ham khoi tao
        public NguoiLaoDong()
        {

        }

        public NguoiLaoDong(string HoTen, short NamSinh, double LuongCoBan)
        {
            this.HoTen = HoTen;
            this.NamSinh = NamSinh;
            this.LuongCoBan = LuongCoBan;
        }

        // Ham
        public void NhapThongTin(string HoTen, short NamSinh, double LuongCoBan)
        {
            this.HoTen = HoTen;
            this.NamSinh = NamSinh;
            this.LuongCoBan = LuongCoBan;
        }

        public virtual double TinhLuong()
        {
            return LuongCoBan;
        }

        public virtual void XuatThongTin()
        {
            Console.WriteLine("Ho ten la: " + HoTen +
                              ", nam sinh: " + NamSinh +
                              ", luong co ban: " + LuongCoBan);
        }
    }
}
