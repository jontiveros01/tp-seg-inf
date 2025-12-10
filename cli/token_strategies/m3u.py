import tkinter.filedialog as fdialog
from pathlib import Path
from cli.settings import get_settings


def m3u(token_uuid):
    """
    Generates MP3 playlist honeytokens (.m3u and .m3u8) that trigger when opened.
    M3U format is universally supported by all Linux media players.
    """
    
    alert_url = f"{get_settings().API_BASE_URL}/api/tokens/alert/{token_uuid}"

    print("Select the source MP3 file (will be referenced in playlist).")
    original_path = fdialog.askopenfilename(
        title="Select MP3 File",
        filetypes=[("MP3 Audio", "*.mp3"), ("All Files", "*.*")]
    )
    
    if not original_path:
        return False

    print("Select directory where to save the playlist honeytokens.")
    output_dir = fdialog.askdirectory(title="Select Output Directory")
    
    if not output_dir:
        return False

    try:
        output_dir = Path(output_dir)
        original_filename = Path(original_path).name
        original_stem = Path(original_path).stem
        
        # === Create M3U Playlist ===
        m3u_path = output_dir / f"{original_stem}.m3u"
        
        # M3U format with honeytoken URLs embedded
        # Format: header line, metadata, URL to fetch, then real file
        m3u_content = f"""#EXTM3U
#EXTINF:-1,{original_stem}
{alert_url}
{original_filename}
"""
        
        with open(m3u_path, 'w', encoding='utf-8') as f:
            f.write(m3u_content)
        
        print(f"✓ Created {m3u_path.name}")
        
        # === Create M3U8 Playlist (HLS/streaming variant) ===
        # Some players specifically look for .m3u8 for streaming content
        m3u8_path = output_dir / f"{original_stem}.m3u8"
        
        with open(m3u8_path, 'w', encoding='utf-8') as f:
            f.write(m3u_content)
        
        print(f"✓ Created {m3u8_path.name}")
        
        print("\n" + "="*70)
        print(f"MP3 Playlist Honeytokens generated successfully!")
        print("="*70)
        print(f"\nFiles created in: {output_dir}")
        print(f"  • {original_stem}.m3u")
        print(f"  • {original_stem}.m3u8")
        print(f"\nHoneytoken UUID: {token_uuid}")
        print(f"\n📝 Note: The playlists reference: {original_filename}")
        print("   Make sure this file exists in the same directory!")
        print(f"\n💡 Tip: Both files work identically. .m3u8 is specifically")
        print("   for players that prefer streaming/HLS formats.")
        
        return True

    except Exception as e:
        print(f"Error generating honeytoken: {e}")
        import traceback
        traceback.print_exc()
        return False