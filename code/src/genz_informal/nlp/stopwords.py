"""Daftar stopword untuk c-TF-IDF (Indonesia + Inggris + token platform).

Dipakai agar kata kunci topik informatif : bukan partikel/kata fungsi.
Catatan: ini HANYA untuk ekstraksi kata kunci (c-TF-IDF), BUKAN untuk input
embedder (embedder tetap memakai teks apa adanya).
"""

from __future__ import annotations

ID = """
yang dan di ke dari untuk dengan pada ini itu saya aku kamu kita kami mereka dia ia
gue gua gw lu lo anda adalah akan sudah belum tidak ga gak nggak tak tak ada juga
bisa dapat harus mau ingin lagi telah sangat lebih paling saja aja sih deh kok ya kan
lah pun nya oleh sebagai atau karena kalau jika ketika saat setelah sebelum sehingga
namun tetapi tapi melainkan bahwa hanya masih pernah sering selalu kadang mungkin
memang akan tersebut para bagi antar hingga sampai sejak dalam antara tentang
bagaimana mengapa kenapa apa siapa mana kapan berapa apakah
""".split()

EN = """
the a an to of in and is it i you my for on with that this be are was were as at by
or not but if from have has had do does did so we they he she them his her its our
your just like know don want get got can could will would should also more most than
then there here what when who how why all any some one two no yes very much many
about into over out up down only other such own same too own
""".split()

PLATFORM = """
removed deleted reddit edit tldr op post posts comment comments thread subreddit sub
karma award imgur http https www amp html utm source medium campaign via com net org
www1 i redd it mods moderator automod bot spam downvote upvote
""".split()

# frasa 2-gram yang tak informatif
PHRASES = ["removed removed", "deleted deleted", "edit tl", "tl dr", "amp amp"]

STOPWORDS = sorted(set(ID) | set(EN) | set(PLATFORM))
