from datetime import datetime

toodolist = []
trash = []
MAX_PIN = 3

kategori_list = ["kuliah", "kerja", "rumah", "penting", "proyek", "lainnya"]
prioritas_list = ["Low", "Medium", "High"]


def ask_yes_no(prompt: str) -> str:
    """
    Minta input konfirmasi 'y' atau 'n'.
    Akan loop sampai user memasukkan 'y' atau 'n' (case-insensitive).
    Mengembalikan 'y' atau 'n'.
    """
    while True:
        jawab = input(prompt).strip().lower()
        if jawab in ("y", "n"):
            return jawab
        print("Pilihan tidak valid! Masukkan 'y' atau 'n'.")


def cek_duplikat(nama):
    for t in toodolist:
        if t["tugas"].lower() == nama.lower():
            return True
    return False


def urutkan_tugas():
    urutan_prioritas = {"High": 1, "Medium": 2, "Low": 3}
    toodolist.sort(
        key=lambda x: (
            not x["pin"],
            urutan_prioritas.get(x.get("priority", "Low"), 3),
            x.get("deadline_dt", datetime.max)
        )
    )


def input_tanggal():
    while True:
        tanggal = input("Masukkan deadline (format YYYY-MM-DD) atau 'batal': ")
        if tanggal.lower() == "batal":
            return None
        try:
            datetime.strptime(tanggal, "%Y-%m-%d")
            return tanggal
        except ValueError:
            print("Tanggal tidak valid! Contoh valid: 2025-02-28\n")


def input_jam():
    while True:
        jam = input("Masukkan jam deadline (format HH:MM) atau 'batal': ")
        if jam.lower() == "batal":
            return None
        try:
            datetime.strptime(jam, "%H:%M")
            return jam
        except ValueError:
            print("Jam tidak valid! Contoh valid: 14:30\n")


def parse_deadline_str_to_dt(deadline_str):
    try:
        return datetime.strptime(deadline_str, "%Y-%m-%d %H:%M")
    except Exception:
        return None


def input_kategori():
    print("\nPilih kategori:")
    for i, k in enumerate(kategori_list, 1):
        print(f"{i}. {k}")
    while True:
        pilih = input("Masukkan nomor kategori: ")
        try:
            pilih = int(pilih)
            if 1 <= pilih <= len(kategori_list):
                return kategori_list[pilih - 1]
            print("Nomor tidak valid!")
        except ValueError:
            print("Masukkan angka yang valid!")


def input_prioritas():
    print("\nPilih prioritas:")
    for i, p in enumerate(prioritas_list, 1):
        print(f"{i}. {p}")
    while True:
        pilih = input("Masukkan nomor prioritas: ")
        try:
            pilih = int(pilih)
            if 1 <= pilih <= len(prioritas_list):
                return prioritas_list[pilih - 1]
            print("Nomor tidak valid!")
        except ValueError:
            print("Masukkan angka valid!")


def tambah_tugas():
    while True:
        tugas = input("Masukkan tugas anda (ketik 'batal' untuk kembali): ")
        if tugas.lower() == "batal":
            print("Kembali ke menu...")
            return
        if cek_duplikat(tugas):
            print("Tugas sudah ada!")
            continue

        created_at_dt = datetime.now()
        created_at = created_at_dt.strftime("%Y-%m-%d %H:%M:%S")

        tanggal = input_tanggal()
        if tanggal is None:
            print("Input dibatalkan...")
            return

        jam = input_jam()
        if jam is None:
            print("Input dibatalkan...")
            return

        deadline_dt = parse_deadline_str_to_dt(f"{tanggal} {jam}")
        if deadline_dt is None:
            print("Format deadline salah.")
            continue

        if deadline_dt <= created_at_dt:
            print("Deadline tidak boleh sebelum atau sama dengan waktu input tugas!")
            continue

        deadline = f"{tanggal} {jam}"
        kategori = input_kategori()
        prioritas = input_prioritas()

        item = {
            "tugas": tugas,
            "status": "belum selesai",
            "pin": False,
            "deadline": deadline,
            "deadline_dt": deadline_dt,
            "created_at": created_at,
            "created_at_dt": created_at_dt,
            "work_time": None,
            "kategori": kategori,
            "priority": prioritas
        }

        toodolist.append(item)
        urutkan_tugas()
        print("Tugas berhasil ditambahkan!")
        return


def lihat_tugas():
    print("----- Tugas Anda -----")
    if len(toodolist) == 0:
        print("Anda tidak memiliki tugas")
        return

    for index, tugas in enumerate(toodolist, 1):
        tanda_pin = "📌" if tugas.get("pin") else "  "
        created = tugas.get("created_at", "-")
        deadline = tugas.get("deadline", "-")
        work_time = tugas.get("work_time")
        work_time_str = work_time.strftime("%Y-%m-%d %H:%M:%S") if work_time else "-"
        print("┌─────────────────────────────────────────────────┐")
        print(f"│              DETAIL TUGAS NOMOR. {index}              │")
        print("├───────────────┬─────────────────────────────────┤")
        print(f"│ Tugas         │ {tugas['tugas']:<24}{tanda_pin}      │")
        print("├───────────────┼─────────────────────────────────┤")
        print(f"│ Kategori      │ {tugas['kategori']:<30}  │")
        print(f"│ Status        │ {tugas['status']:<30}  │")
        print(f"│ Created       │ {created:<30}  │")
        print(f"│ Deadline      │ {deadline:<30}  │")
        print(f"│ Waktu Kerja   │ {work_time_str:<30}  │")
        print(f"│ Prioritas     │ {tugas.get('priority','-'):<30}  │")
        print("└─────────────────────────────────────────────────┘")


def cari_tugas():
    if len(toodolist) == 0:
        print("Anda tidak memiliki tugas!")
        return

    while True:
        keyword = input("Masukkan kata kunci pencarian (ketik 'batal' untuk kembali): ")
        if keyword.lower() == "batal":
            print("Kembali ke menu...")
            return

        hasil = []
        for index, t in enumerate(toodolist, 1):
            if keyword.lower() in t["tugas"].lower():
                hasil.append((index, t))

        if len(hasil) == 0:
            print("Tidak ada tugas yang cocok.")
        else:
            print("\n===== HASIL PENCARIAN =====")
            for index, tugas in hasil:
                tanda_pin = "📌" if tugas.get("pin") else " "
                created = tugas.get("created_at", "-")
                deadline = tugas.get("deadline", "-")
                work_time = tugas.get("work_time")
                work_time_str = work_time.strftime("%Y-%m-%d %H:%M:%S") if work_time else "-"

                print("┌─────────────────────────────────────────────────┐")
                print(f"│            DETAIL TUGAS (No. {index})                 │")
                print("├───────────────┬─────────────────────────────────┤")
                print(f"│ Tugas         │ {tugas['tugas']:<24}{tanda_pin}      │")
                print("├───────────────┼─────────────────────────────────┤")
                print(f"│ Kategori      │ {tugas['kategori']:<30}  │")
                print(f"│ Status        │ {tugas['status']:<30}  │")
                print(f"│ Created       │ {created:<30}  │")
                print(f"│ Deadline      │ {deadline:<30}  │")
                print(f"│ Waktu Kerja   │ {work_time_str:<30}  │")
                print(f"│ Prioritas     │ {tugas.get('priority','-'):<30}  │")
                print("└─────────────────────────────────────────────────┘\n")


def lihat_sampah():
    print("\n===== TUGAS DI DALAM SAMPAH =====")
    if len(trash) == 0:
        print("Sampah kosong.")
    else:
        for i, t in enumerate(trash, 1):
            print("┌─────────────────────────────────────────────────┐")
            print(f"│              SAMPAH TUGAS NOMOR. {i}              │")
            print("├───────────────┬─────────────────────────────────┤")
            print(f"│ Tugas         │ {t['tugas']:<30}  │")
            print("├───────────────┼─────────────────────────────────┤")
            print(f"│ Kategori      │ {t['kategori']:<30}  │")
            print(f"│ Status        │ {t['status']:<30}  │")
            print(f"│ Created       │ {t.get('created_at','-'):<30}  │")
            print(f"│ Deadline      │ {t.get('deadline','-'):<30}  │")
            print("└─────────────────────────────────────────────────┘\n")


def restore_tugas():
    if len(trash) == 0:
        print("Sampah kosong, tidak ada yang bisa di-restore.")
        return

    lihat_sampah()
    while True:
        pilih = input("Masukkan nomor tugas yang ingin di-restore (ketik 'batal'): ")
        if pilih.lower() == "batal":
            print("Kembali ke menu...")
            return
        try:
            pilih = int(pilih) - 1
            if 0 <= pilih < len(trash):
                tugas_restore = trash.pop(pilih)
                tugas_restore["pin"] = False
                if "deadline_dt" in tugas_restore and isinstance(tugas_restore["deadline_dt"], str):
                    tugas_restore["deadline_dt"] = parse_deadline_str_to_dt(tugas_restore["deadline"])
                toodolist.append(tugas_restore)
                urutkan_tugas()
                print(f"Tugas '{tugas_restore['tugas']}' telah dikembalikan!")
                return
            print("Nomor tidak valid!")
        except ValueError:
            print("Masukkan nomor valid!")


def hapus_tugas():
    if len(toodolist) == 0:
        print("Anda tidak memiliki tugas!")
        return

    lihat_tugas()
    while True:
        hapus = input("Masukkan nomor tugas yang ingin dihapus (ketik 'batal'): ")
        if hapus.lower() == "batal":
            print("Batal menghapus, kembali ke menu...")
            return
        try:
            hapus = int(hapus) - 1
            if 0 <= hapus < len(toodolist):
                konfirmasi = ask_yes_no(
                    f"Yakin ingin menghapus '{toodolist[hapus]['tugas']}'? (y/n): "
                )
                if konfirmasi == "y":
                    tugas_hapus = toodolist.pop(hapus)
                    trash.append(tugas_hapus)
                    urutkan_tugas()
                    print(f"Tugas dipindahkan ke Sampah: {tugas_hapus['tugas']}")
                else:
                    print("Penghapusan dibatalkan.")
                return
            print("Nomor tugas tidak valid.")
        except ValueError:
            print("Masukkan nomor yang valid!")


def edit_tugas():
    if len(toodolist) == 0:
        print("Anda tidak memiliki tugas!")
        return

    lihat_tugas()
    while True:
        pilih = input("Masukkan nomor tugas yang ingin diedit (ketik 'batal'): ")
        if pilih.lower() == "batal":
            print("Batal edit, kembali ke menu...")
            return
        try:
            pilih = int(pilih) - 1
            if 0 <= pilih < len(toodolist):
                tugas = toodolist[pilih]

                while True:
                    print("\n--- MENU EDIT ---")
                    print("1. Nama Tugas")
                    print("2. Deadline")
                    print("3. Kategori")
                    print("4. Prioritas")
                    print("5. Status")
                    print("6. Pin atau Unpin")
                    print("7. Kembali")

                    opsi = input("Pilih bagian: ")

                    if opsi == "1":
                        nama_baru = input("Masukkan nama tugas baru: ")
                        if cek_duplikat(nama_baru):
                            print("Tugas dengan nama itu sudah ada!")
                            continue
                        tugas["tugas"] = nama_baru
                        print("Nama tugas berhasil diubah!")

                    elif opsi == "2":
                        tanggal = input_tanggal()
                        if tanggal is None:
                            print("Edit dibatalkan.")
                            continue
                        jam = input_jam()
                        if jam is None:
                            print("Edit dibatalkan.")
                            continue
                        new_deadline_dt = parse_deadline_str_to_dt(f"{tanggal} {jam}")
                        if new_deadline_dt is None:
                            print("Format deadline salah.")
                            continue
                        created_dt = tugas.get("created_at_dt") or datetime.strptime(tugas.get("created_at"), "%Y-%m-%d %H:%M:%S")
                        if new_deadline_dt <= created_dt:
                            print("Deadline baru tidak boleh sebelum atau sama dengan waktu input tugas!")
                            continue
                        tugas["deadline"] = f"{tanggal} {jam}"
                        tugas["deadline_dt"] = new_deadline_dt
                        print("Deadline berhasil diubah!")

                    elif opsi == "3":
                        kategori_baru = input_kategori()
                        tugas["kategori"] = kategori_baru
                        print("Kategori berhasil diubah!")

                    elif opsi == "4":
                        print("\nPilih Prioritas:")
                        print("1. High")
                        print("2. Medium")
                        print("3. Low")
                        pilih_prioritas = input("Masukkan pilihan: ")
                        mapping = {"1": "High", "2": "Medium", "3": "Low"}
                        if pilih_prioritas in mapping:
                            tugas["priority"] = mapping[pilih_prioritas]
                            urutkan_tugas()
                            print("Prioritas diubah!")
                        else:
                            print("Pilihan tidak valid!")

                    elif opsi == "5":
                        print("\nUbah status:")
                        print("1. Selesai")
                        print("2. Belum selesai")
                        st = input("Masukkan pilihan: ")
                        if st == "1":
                            tugas["status"] = "selesai"
                        elif st == "2":
                            tugas["status"] = "belum selesai"
                        else:
                            print("Pilihan tidak valid!")
                            continue
                        print("Status berhasil diubah!")

                    elif opsi == "6":
                        pinned_count = sum(1 for t in toodolist if t["pin"])
                        if tugas["pin"]:
                            lepas = ask_yes_no("Tugas sudah di-pin. Lepas pin? (y/n): ")
                            if lepas == "y":
                                tugas["pin"] = False
                                print("Pin dilepas.")
                        else:
                            if pinned_count >= MAX_PIN:
                                print(f"Maksimal pin adalah {MAX_PIN}! Lepas pin lain sebelum menambah.")
                            else:
                                pasang = ask_yes_no("Ingin mem-pin tugas ini? (y/n): ")
                                if pasang == "y":
                                    tugas["pin"] = True
                                    print("Tugas di-pin.")
                        urutkan_tugas()

                    elif opsi == "7":
                        print("Kembali ke menu utama...")
                        return

                    else:
                        print("Pilihan tidak valid!")
            else:
                print("Nomor tidak valid!")
        except ValueError:
            print("Masukkan nomor yang valid!")


def tugas_selesai():
    if len(toodolist) == 0:
        print("Anda tidak memiliki tugas!")
        return

    while True:
        lihat_tugas()
        selesai = input("Masukkan nomor tugas yang ingin ditandai selesai (ketik 'batal'): ")
        if selesai.lower() == "batal":
            print("Batal menandai, kembali ke menu...")
            return
        try:
            selesai = int(selesai) - 1
            if 0 <= selesai < len(toodolist):
                if toodolist[selesai]["status"] == "selesai":
                    print(f"Tugas '{toodolist[selesai]['tugas']}' sudah selesai!")
                    ubah = ask_yes_no("Ubah menjadi belum selesai? (y/n): ")
                    if ubah == "y":
                        toodolist[selesai]["status"] = "belum selesai"
                        print("Status diubah.")
                        return
                    continue
                konfirmasi = ask_yes_no(
                    f"Yakin ingin menandai '{toodolist[selesai]['tugas']}' sebagai selesai? (y/n): "
                )
                if konfirmasi == "y":
                    toodolist[selesai]["status"] = "selesai"
                    print(f"Tugas '{toodolist[selesai]['tugas']}' telah ditandai selesai.")
                return
            print("Nomor tugas tidak ada!")
        except ValueError:
            print("Masukkan nomor yang valid!")


def pin_tugas():
    if len(toodolist) == 0:
        print("Anda tidak memiliki tugas!")
        return

    pinned_count = sum(1 for t in toodolist if t["pin"])

    lihat_tugas()
    while True:
        pilih = input("Masukkan nomor tugas yang ingin di-pin (ketik 'batal'): ")
        if pilih.lower() == "batal":
            print("Batal, kembali ke menu...")
            return
        try:
            pilih = int(pilih) - 1
            if 0 <= pilih < len(toodolist):

                if toodolist[pilih]["pin"]:
                    un = ask_yes_no("Tugas sudah di-pin. Lepas pin? (y/n): ")
                    if un == "y":
                        toodolist[pilih]["pin"] = False
                        urutkan_tugas()
                        print("Pin dilepas!")
                    return

                if pinned_count >= MAX_PIN:
                    print(f"Anda sudah mem-pin {MAX_PIN} tugas! Lepas pin salah satu dulu.")
                    return

                konfirmasi = ask_yes_no(
                    f"Ingin mem-pin '{toodolist[pilih]['tugas']}'? (y/n): "
                )

                if konfirmasi == "y":
                    toodolist[pilih]["pin"] = True
                    urutkan_tugas()
                    print("Tugas berhasil di-pin!")
                else:
                    print("Pin dibatalkan.")
                return
            print("Nomor tidak valid.")
        except ValueError:
            print("Masukkan nomor valid!")


def mulai_kerjakan():
    if len(toodolist) == 0:
        print("Tidak ada tugas untuk dikerjakan.")
        return

    lihat_tugas()
    while True:
        pilih = input("Masukkan nomor tugas yang ingin dikerjakan (ketik 'batal'): ")
        if pilih.lower() == "batal":
            print("Batal, kembali ke menu...")
            return
        try:
            pilih = int(pilih) - 1
            if 0 <= pilih < len(toodolist):
                tugas = toodolist[pilih]
                now = datetime.now()
                deadline_dt = tugas.get("deadline_dt") or parse_deadline_str_to_dt(tugas.get("deadline", ""))
                if deadline_dt is None:
                    print("Deadline tidak valid, tidak bisa dikerjakan.")
                    return
                if now > deadline_dt:
                    print("Waktu pengerjaan sudah lewat deadline! Tidak bisa dikerjakan.")
                    return
                tugas["work_time"] = now
                tugas["work_time_str"] = now.strftime("%Y-%m-%d %H:%M:%S")
                print(f"Mulai mengerjakan '{tugas['tugas']}' pada {tugas['work_time_str']}")
                return
            print("Nomor tugas tidak ada!")
        except ValueError:
            print("Masukkan nomor yang valid!")


def menu():
    while True:
        print("┌──────────────────────────────────────────┐")
        print("│                 MAIN MENU                │")
        print("├───────────┬──────────────────────────────┤")
        print("│ No.       │ Menu                         │")
        print("├───────────┼──────────────────────────────┤")
        print("│ 1         │ Tambah Tugas                 │")
        print("│ 2         │ Lihat Semua Tugas            │")
        print("│ 3         │ Cari Tugas                   │")
        print("│ 4         │ Mulai Kerjakan Tugas         │")
        print("│ 5         │ Tandai Tugas Selesai         │")
        print("│ 6         │ Edit Tugas                   │")
        print("│ 7         │ Pin / Sematkan Tugas         │")
        print("│ 8         │ Hapus / Pindah ke Sampah     │")
        print("│ 9         │ Lihat Sampah                 │")
        print("│ 10        │ Restore Tugas dari Sampah    │")
        print("│ 11        │ Keluar                       │")
        print("└──────────────────────────────────────────┘")

        pilih = input("Masukkan pilihan anda: ")

        if pilih == "1":
            tambah_tugas()
        elif pilih == "2":
            lihat_tugas()
        elif pilih == "3":
            cari_tugas()
        elif pilih == "4":
            mulai_kerjakan()
        elif pilih == "5":
            tugas_selesai()
        elif pilih == "6":
            edit_tugas()
        elif pilih == "7":
            pin_tugas()
        elif pilih == "8":
            hapus_tugas()
        elif pilih == "9":
            lihat_sampah()
        elif pilih == "10":
            restore_tugas()
        elif pilih == "11":
            print("Keluar dari to do list...")
            break
        else:
            print("Pilihan tidak valid!")


if _name_ == "_main_":
    menu()
