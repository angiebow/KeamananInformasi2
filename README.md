# Keamanan Informasi 2

```
⁠Implementasi transfer string terenkripsi antar 2 user menggunakan socket programming (penerima dapat mendekripsi string dari pengirim)
⁠Enkripsi dan Dekripsi harus bisa menerima input lebih dari 64bit (8 karakter)
String enkripsi wajib dikirimkan melalui socket (tidak boleh read/write file)
⁠Untuk key dianggap 2 client tau(boleh hardcode)
```

# Keamanan Informasi 3
```
Pengembangan program Percakapan antara dua perangkat dari Tugas 2:
1.⁠ ⁠Implementasi Pengiriman key DES pada percakapan menggunakan algoritma RSA
2.⁠ ⁠Public key dari RSA harus diperoleh melalui Public Key Authority
3.⁠ ⁠Pengiriman Key DES harus menggunakan Public-Key Cryptosystems

Program flow
	•	Jalankan pka.py terlebih dahulu untuk menghasilkan kunci.
	•	Salin public.pem ke direktori client dan server.

  1.	PKA membuat pasangan kunci RSA (public & private).
	2.	Client mendapatkan public.pem dari PKA dan mengenkripsi kunci DES menggunakan public key RSA.
	3.	Client mengirim kunci DES terenkripsi ke server.
	4.	Server menerima kunci DES terenkripsi, mendekripsinya menggunakan private key RSA, dan menggunakan kunci DES untuk komunikasi selanjutnya.
```
