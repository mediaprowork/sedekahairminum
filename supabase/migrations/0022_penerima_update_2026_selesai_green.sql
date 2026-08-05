-- 0022_penerima_update_2026_selesai_green.sql
-- CATATAN UPDATE 2026 (latest brief). Two more pondok are now SELESAI
-- tersalurkan and must render red in the /penerima table and faded-GREEN on the
-- map (marker color handled in IndonesiaMap.tsx):
--   * PP Hidayatul Mubtadiin Kunci
--   * PP Muhammadiyah Al-Mujahidin
-- Per the brief ("yang selesai tersalurkan tolong taruh di bawah"), ALL selesai
-- pondok are sorted to the bottom of the table: 15 tersalurkan (sort 1-15) then
-- 6 selesai (sort 16-21). Coords are preserved so every row keeps its map dot.
-- Also bumps the Galon/Distribusi counter to 1.984 (home + penerima).
-- Idempotent (by name/label). Source: gdoc 16BHgxfZ77YxF3Q0z_IKwnsSRaM-XfIMWttmXCEe4lGE.

-- Two more finished pondok -> selesai (red in table, faded green on map).
update public.penerima set status='selesai', is_published=true
  where name='PP Hidayatul Mubtadiin Kunci';
update public.penerima set status='selesai', is_published=true
  where name='PP Muhammadiyah Al-Mujahidin';

-- Tersalurkan first (1-15), keeping the brief's relative order.
update public.penerima set sort_order=1  where name='PP An-Nur';
update public.penerima set sort_order=2  where name='PP Fajrussa''adah';
update public.penerima set sort_order=3  where name='PP Al-Kholifah';
update public.penerima set sort_order=4  where name='PP Al-Murtadlo';
update public.penerima set sort_order=5  where name='PP Ar-Ruhamaa''';
update public.penerima set sort_order=6  where name='Pondok Nurul Jamil Al-Jumar';
update public.penerima set sort_order=7  where name='PP Nurulhadi 2';
update public.penerima set sort_order=8  where name='PP Ainul Yakin Special Children';
update public.penerima set sort_order=9  where name='PP & Islamic Center Yasma Mulia';
update public.penerima set sort_order=10 where name='PP Roudlotuth Tholabah';
update public.penerima set sort_order=11 where name='Nurul Qur''an Islamic Boarding School';
update public.penerima set sort_order=12 where name='PP Kun Solihan';
update public.penerima set sort_order=13 where name='Yayasan Panti Asuhan Islam';
update public.penerima set sort_order=14 where name='PP Thoriqul Mukminin';
update public.penerima set sort_order=15 where name='PP Ash-Shiddiq 2';

-- Selesai at the bottom (16-21).
update public.penerima set sort_order=16 where name='PP Hidayatul Mubtadiin Kunci';
update public.penerima set sort_order=17 where name='PP Muhammadiyah Al-Mujahidin';
update public.penerima set sort_order=18 where name='PP KI Ageng Wonokusumo';
update public.penerima set sort_order=19 where name='PP Baitul Jannah Darussalam';
update public.penerima set sort_order=20 where name='PP Assalafiyah Darussalam';
update public.penerima set sort_order=21 where name='PP Al-Hikmah Gubuk Rubuh';

-- Stats (home + penerima): Galon/Distribusi 1446 -> 1984; others re-asserted.
update public.stats set num=1    where label in ('Kabupaten','Kabupaten Aktif');
update public.stats set num=21   where label='Lembaga Penerima';
update public.stats set num=1984 where label='Galon/Distribusi';
update public.stats set num=9    where label in ('Kecamatan','Kecamatan Terjangkau');
