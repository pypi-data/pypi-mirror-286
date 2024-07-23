import os
import sys
from mutagen.id3 import ID3, ID3NoHeaderError, APIC, TCMP, TIT2, TPE1, TALB, TDRC, TCON, TRCK, TPOS

'''
    cd_tracks 출처: https://gall.dcinside.com/mini/board/view/?id=musicalplay&no=216401
'''

def get_mime_type(file_path):
    # Estimate MIME type from file path.
    import mimetypes
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type if mime_type else 'image/jpeg'  # 기본 MIME 타입을 'image/jpeg'로 설정

def update_mp3_metadata(mp3_file, track, title, artist, album, year, genre, discnumber, image_path=None):
    try:
        # Load or create ID3 tags
        if not os.path.isfile(mp3_file):
            print(f"파일 {mp3_file}이 존재하지 않습니다.")
        
        try:
            audio = ID3(mp3_file)
        except ID3NoHeaderError:
            audio = ID3()

        # Set or update tags
        audio.add(TIT2(encoding=3, text=title))  # Title
        audio.add(TPE1(encoding=3, text=artist))  # Artist
        audio.add(TALB(encoding=3, text=album))   # Album
        audio.add(TDRC(encoding=3, text=year))     # Year
        audio.add(TCON(encoding=3, text=genre))    # Genre
        audio.add(TRCK(encoding=3, text=track))    # Track number
        audio.add(TPOS(encoding=3, text=discnumber)) # Disc number

        # Add or update TCMP (compilation) tag
        audio.delall('TCMP')
        audio.add(TCMP(encoding=3, text='1'))

        # Add or update album art
        if image_path:
            print(image_path)
            mime_type = get_mime_type(image_path)
            audio.delall('APIC')
            with open(image_path, 'rb') as img:
                audio.add(APIC(
                    encoding=3,  # UTF-8
                    mime=mime_type,  # MIME type
                    type=3,  # Album art
                    desc='Cover',
                    data=img.read()
                ))

        audio.save(mp3_file)
        print(f"Updated metadata for {mp3_file}")

    except Exception as e:
        print(f"Failed to update {mp3_file}: {e}")

def main(folder_path, album_name, image_path=None):
    cd_tracks = {
        '1': [
            ("01", "프롤로그(Prologue)", "VAMPIRE SLAVE, ENSEMBLE"),
            ("02", "잊혀진 존재(Solitary Man)", "김준수"),
            ("03", "휘트비 베이(Whitby Bay)", "임혜영, 진태화"),
            ("04", "영원한 젊음(Forever Young)", "진태화, VAMPIRE SLAVE"),
            ("05", "신선한 피(Fresh Blood)", "김준수, VAMPIRE SLAVE, ENSEMBLE"),
            ("06", "주인님의 노래(The Master's Song)", "손준호, 김도현, VAMPIRE SLAVE, ENSEMBLE"),
            ("07", "최후의 승자(Last Man Standing)", "손준호"),
            ("08", "모르겠어(How Do You Choose)", "임혜영, 이예은, 이재현, 민준호, 이호진, ENSEMBLE"),
            ("09", "안개 속으로(The Mist)", "이예은"),
            ("10", "그녀(She)", "김준수"),
            ("11", "완벽한 인생 / 그댄 내 삶의 이유 / 휘트비 베이(리프라이즈)(A Perfect Life / Loving You Keeps Me Alive / Whitby Bay(Reprise))", "김준수, 임혜영, 진태화"),
            ("12", "초대(The Invitation)", "이예은"),
            ("13", "영원한 삶(Life After Life)", "김준수, 이예은, VAMPIRE SLAVE, ENSEMBLE"),
            ("14", "사랑하면 안돼(Please Don't Make Me Love You)", "임혜영"),
            ("15", "하늘 위로(If I Had Wings)", "임혜영"),
            ("16", "미나의 유혹(Mina's Seduction)", "김준수, 임혜영"),
            ("17", "다 끝났어(It's Over)", "김준수, 손준호"),
            ("18", "여름이 끝나기 전(Before The Summer Ends)", "진태화"),
            ("19", "트레인 시퀀스(Train Sequence)", "김준수, 임혜영, 손준호"),
            ("20", "검붉은 어둠(Deep in the Darkest Night)", "김준수, 손준호, 진태화, 이재현, 민준호, 이호진, ENSEMBLE"),
            ("21", "그대 없는 영원(The Longer I Live)", "김준수"),
            ("22", "이제(At Last)", "김준수, 임혜영"),
            ("23", "피날레(Finale)", "김준수, 임혜영"),
            ("24", "커튼콜(Bows)", "inst.")
        ],
        '2': [
            ("01", "프롤로그(Prologue)", "VAMPIRE SLAVE, ENSEMBLE"),
            ("02", "잊혀진 존재(Solitary Man)", "전동석"),
            ("03", "휘트비 베이(Whitby Bay)", "정선아, 임준혁"),
            ("04", "영원한 젊음(Forever Young)", "임준혁, VAMPIRE SLAVE"),
            ("05", "신선한 피(Fresh Blood)", "전동석, VAMPIRE SLAVE, ENSEMBLE"),
            ("06", "주인님의 노래(The Master's Song)", "박은석, 김도하, VAMPIRE SLAVE, ENSEMBLE"),
            ("07", "최후의 승자(Last Man Standing)", "박은석"),
            ("08", "모르겠어(How Do You Choose)", "정선아, 최서연, 이재현, 민준호, 이호진, ENSEMBLE"),
            ("09", "안개 속으로(The Mist)", "최서연"),
            ("10", "그녀(She)", "전동석"),
            ("11", "완벽한 인생 / 그댄 내 삶의 이유 / 휘트비 베이(리프라이즈)(A Perfect Life / Loving You Keeps Me Alive / Whitby Bay(Reprise))", "전동석, 정선아, 임준혁"),
            ("12", "초대(The Invitation)", "최서연"),
            ("13", "영원한 삶(Life After Life)", "전동석, 최서연, VAMPIRE SLAVE, ENSEMBLE"),
            ("14", "사랑하면 안돼(Please Don't Make Me Love You)", "정선아"),
            ("15", "하늘 위로(If I Had Wings)", "정선아"),
            ("16", "미나의 유혹(Mina's Seduction)", "전동석, 정선아"),
            ("17", "다 끝났어(It's Over)", "전동석, 박은석"),
            ("18", "여름이 끝나기 전(Before The Summer Ends)", "임준혁"),
            ("19", "트레인 시퀀스(Train Sequence)", "전동석, 정선아, 박은석"),
            ("20", "검붉은 어둠(Deep in the Darkest Night)", "전동석, 박은석, 임준혁, 이재현, 민준호, 이호진, ENSEMBLE"),
            ("21", "그대 없는 영원(The Longer I Live)", "전동석"),
            ("22", "이제(At Last)", "전동석, 정선아"),
            ("23", "피날레(Finale)", "전동석, 정선아"),
            ("24", "커튼콜(Bows)", "inst.")
        ],
        '3': [
            ("01", "프롤로그(Prologue)", "VAMPIRE SLAVE, ENSEMBLE"),
            ("02", "잊혀진 존재(Solitary Man)", "신성록"),
            ("03", "휘트비 베이(Whitby Bay)", "아이비, 진태화"),
            ("04", "영원한 젊음(Forever Young)", "진태화, VAMPIRE SLAVE"),
            ("05", "신선한 피(Fresh Blood)", "신성록, VAMPIRE SLAVE, ENSEMBLE"),
            ("06", "주인님의 노래(The Master's Song)", "손준호, 김도현, VAMPIRE SLAVE, ENSEMBLE"),
            ("07", "최후의 승자(Last Man Standing)", "손준호"),
            ("08", "모르겠어(How Do You Choose)", "아이비, 이예은, 이재현, 민준호, 이호진, ENSEMBLE"),
            ("09", "안개 속으로(The Mist)", "이예은"),
            ("10", "그녀(She)", "신성록"),
            ("11", "완벽한 인생 / 그댄 내 삶의 이유 / 휘트비 베이(리프라이즈)(A Perfect Life / Loving You Keeps Me Alive / Whitby Bay(Reprise))", "신성록, 아이비, 진태화"),
            ("12", "초대(The Invitation)", "이예은"),
            ("13", "영원한 삶(Life After Life)", "신성록, 이예은, VAMPIRE SLAVE, ENSEMBLE"),
            ("14", "사랑하면 안돼(Please Don't Make Me Love You)", "아이비"),
            ("15", "하늘 위로(If I Had Wings)", "아이비"),
            ("16", "미나의 유혹(Mina's Seduction)", "신성록, 아이비"),
            ("17", "다 끝났어(It's Over)", "신성록, 손준호"),
            ("18", "여름이 끝나기 전(Before The Summer Ends)", "진태화"),
            ("19", "트레인 시퀀스(Train Sequence)", "신성록, 아이비, 손준호"),
            ("20", "검붉은 어둠(Deep in the Darkest Night)", "신성록, 손준호, 진태화, 이재현, 민준호, 이호진, ENSEMBLE"),
            ("21", "그대 없는 영원(The Longer I Live)", "신성록"),
            ("22", "이제(At Last)", "신성록, 아이비"),
            ("23", "피날레(Finale)", "신성록, 아이비"),
            ("24", "커튼콜(Bows)", "inst.")
        ]
    }

    # Loop through CD tracks and update metadata
    for cd_number, tracks in cd_tracks.items():
        for track, title, artist in tracks:
            # Construct file path
            # mp3_file = os.path.join(folder_path, f"CD{cd_number}/{format(track, '02')} 트랙 {track}.mp3")
            mp3_file = os.path.join(folder_path, f"CD{cd_number}", f"{format(track, '02')} 트랙 {int(track)}.mp3")
            
            update_mp3_metadata(
                mp3_file,
                track,
                title,
                artist,
                album_name,
                "2024",
                "MUSICAL",
                cd_number,
                image_path
            )
