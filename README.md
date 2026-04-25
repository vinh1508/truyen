# truyen

Generate lai danh sach chuong:

```sh
python3 scripts/generate_chapters.py
```

Script se quet cac thu muc con trong `truyen/`, doc title tu dong `# ...` dau tien cua moi file `.md`, roi cap nhat `chapters.json`.

Git hook truoc khi push:

```sh
git config core.hooksPath scripts/hooks
```

Sau khi bat hook, moi lan `git push` se tu chay lenh generate tren. Neu `chapters.json` thay doi, hook se tu commit cac thay doi trong `truyen/` cung manifest moi, roi dung push hien tai de ban chay `git push` lai voi commit moi.

Neu muon mot lenh tu generate, commit, roi push luon:

```sh
scripts/push.sh origin main:main
```


*(Bản dịch được hiệu chỉnh theo hướng kết hợp yếu tố Khoa Huyễn/Vũ Trụ: nhấn mạnh vào "trường lực", "cấu trúc đa chiều", "dữ liệu quỹ đạo", "không thời gian", đồng thời giữ nguyên hệ thống cảnh giới và thuật ngữ Huyền Ảo gốc để đảm bảo tính nhất quán với nguyên tác.)*
