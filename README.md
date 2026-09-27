
Nama  : Aisyah Putri Nur Afifah
NIM   : 20240801143
Kelas : KH001
Mata Kuliah : Game Development

# 🎀 Hello Kitty: Dungeon Escape

Game sederhana berbasis Python menggunakan Pygame.
Player harus bergerak di dalam dungeon untuk mencapai
pintu keluar, sambil menghindari monster yang dapat
mendeteksi dan mengejarnya menggunakan algoritma AI.

**Tujuan permainan:** mencapai pintu keluar tanpa tertangkap monster.

---

## 1. Identifikasi Algoritma yang Digunakan

### A. Manhattan Distance (Deteksi Player)

Manhattan Distance digunakan untuk menghitung jarak
antara monster dan player. Jika player berada dalam
jangkauan deteksi, monster akan mulai mengejarnya.

Rumus:

`d = |x1 - x2| + |y1 - y2|`

Pada game ini, monster mendeteksi player jika jaraknya
kurang dari atau sama dengan 20.

### B. A* (A-Star) Pathfinding

Algoritma A* digunakan untuk mencari jalur dari posisi
monster menuju player dengan menghindari dinding
atau rintangan di dalam dungeon.

A* mempertimbangkan jarak yang sudah ditempuh dan
perkiraan jarak menuju tujuan untuk menentukan jalur.

### C. Rule-Based Movement

Rule-Based Movement digunakan untuk mengatur kecepatan
monster berdasarkan jaraknya dari player.

- Jarak lebih dari 8: kecepatan normal.
- Jarak 4–8: kecepatan mengejar.
- Jarak 0–3: kecepatan cepat.

Semakin dekat monster dengan player, semakin cepat
monster bergerak.

### D. Game Loop

Game Loop digunakan untuk menjalankan permainan
secara berulang, mulai dari membaca input keyboard,
memperbarui posisi player dan monster, menjalankan
algoritma AI, hingga menampilkan tampilan game.


---

## 2. Flowchart

Flowchart berikut menggambarkan proses permainan,
mulai dari inisialisasi dungeon, pergerakan player,
deteksi monster, pencarian jalur menggunakan A*,
hingga kondisi menang atau kalah.

![Flowchart Hello Kitty Dungeon Escape](Flowchart%20Game%20Development.jpg)


---

## 3. Code Snippet

Berikut adalah potongan kode yang digunakan untuk
mendeteksi player, menentukan kecepatan monster,
dan mencari jalur menggunakan algoritma A*.

```python
distance = manhattan_distance(enemy, player)

if distance <= DETECTION_RANGE:
    if distance <= 3:
        move_delay = ANGRY_SPEED
    elif distance <= 8:
        move_delay = CHASE_SPEED
    else:
        move_delay = NORMAL_SPEED

    enemy_path = astar(enemy, player)
```

Kode lengkap game dapat dilihat pada file
`hello_kitty_dungeon.py`.