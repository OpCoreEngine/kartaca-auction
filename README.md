# Açık Artırma Uygulaması

Bu proje, kullanıcıların ürünler üzerinde canlı olarak açık artırma yapabileceği ve teklif sunabileceği basit bir web uygulamasıdır. Arka uç için Flask (Python) kullanılırken, ön yüz için Vue.js kullanılmıştır. Oturum bilgileri için Redis kullanılırken, veritabanı olarak PostgreSQL tercih edilmiştir.

## Özellikler

* Kullanıcı üyeliği, oturum açma ve oturum kapatma
* Anasayfada oturum açan kullanıcılar için 3 adet ürün görüntüleme
* Oturum açmamış kullanıcılar için oturum açma sayfasına yönlendirme
* Canlı açık artırma yapabilme ve teklif sunabilme
* Diğer kullanıcıların canlı olarak açık artırmayı takip etme ve güncel fiyatı görebilme
* Güvenlik ve Oturum Yönetimi
* Kullanıcı parolaları şifrelenmiş şekilde saklanır (bcrypt kullanılarak)
* JSON Web Token (JWT) ile güvenli oturum yönetimi

## Kurulum

### Gereksinimler

* Docker ve Docker Compose kurulu olmalıdır.

### Adımlar

1. Bu GitHub reposunu klonlayın veya indirin.
2. Klonlanan veya indirilen dizine gidin.
3. `.env.example` dosyasını `.env` olarak yeniden adlandırın ve içerisindeki gerekli değişkenleri doldurun.
4. Terminalde (veya komut istemcisinde) aşağıdaki komutu çalıştırarak uygulamayı başlatın:
`docker-compose up -d`
5. Tarayıcınızda http://localhost:8080 adresini açarak uygulamayı kullanmaya başlayabilirsiniz.


## Kullanım

1. Kayıt olun veya oturum açın.
2. Anasayfada görünen ürünler üzerinde açık artırmaya katılabilirsiniz.
3. Başka kullanıcılar da açık artırmaya katıldığında, sayfayı yenilemeden güncel fiyatları ve son teklif veren kullanıcıyı görebilirsiniz.
4. Oturumu kapatmak için "Çıkış Yap" seçeneğini kullanabilirsiniz.

## Görev İçeriği Erişimi

Görev içeriğine ulaşmak için kullanılan kod, `Kartaca-Task-Content-Access` klasöründe bulunabilir

`"registrationKey": "532dc0cf3de3e4cb34e199d056cfff59cab4440e8fbf4f6ea9a8705a0a986eba"`
