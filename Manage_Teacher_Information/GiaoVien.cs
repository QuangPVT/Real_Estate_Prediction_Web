using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Manage_Teacher_Information
{
    public class GiaoVien : NguoiLaoDong
    {
        // Thuoc tinh
        public double HeSoLuong;

        // Ham
        public GiaoVien()
        {

        }

        public GiaoVien(string HoTen, short NamSinh, double LuongCoBan, double HeSoLuong)
        : base(HoTen, NamSinh, LuongCoBan)
        {
            this.HeSoLuong = HeSoLuong;
        }

        public void NhapThongTin(double HeSoLuong)
        {
            this.HeSoLuong = HeSoLuong;
        }

        public override double TinhLuong()
        {
            return LuongCoBan * HeSoLuong * 1.25;
        }
        
        public override void XuatThongTin()
        {
            Console.WriteLine("Ho ten la: " + HoTen +
                              ", nam sinh: " + NamSinh +
                              ", luong co ban: " + LuongCoBan +
                              ", he so luong: " + HeSoLuong +
                              ", luong: " + TinhLuong());
        }

        public void XyLy()
        {
            this.HeSoLuong = HeSoLuong + 0.6;
        }
    }
}
