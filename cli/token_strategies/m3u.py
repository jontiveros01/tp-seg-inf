import tkinter.filedialog as fdialog
from pathlib import Path
from cli.settings import get_settings


def m3u(token_uuid, playlist_format):
    """
    Generates MP3 playlist honeytoken that triggers when opened.
    
    Args:
        token_uuid: Unique identifier for the honeytoken
        playlist_format: Either 'm3u', 'm3u8', or 'both'
    """
    
    alert_url = f"{get_settings().API_BASE_URL}/api/tokens/alert/{token_uuid}"

    print("Select the source MP3 file (will be referenced in playlist).")
    original_path = fdialog.askopenfilename(
        title="Select MP3 File",
        filetypes=[("MP3 Audio", "*.mp3"), ("All Files", "*.*")]
    )
    
    if not original_path:
        return False

    print("Select directory where to save the playlist honeytoken(s).")
    output_dir = fdialog.askdirectory(title="Select Output Directory")
    
    if not output_dir:
        return False

    try:
        output_dir = Path(output_dir)
        original_filename = Path(original_path).name
        original_stem = Path(original_path).stem
        
        # M3U content (same for both formats)
        m3u_content = f"""#EXTM3U
#EXTINF:-1,{original_stem}
{alert_url}
{original_filename}
"""
        
        files_created = []
        
        # Create M3U if requested
        if playlist_format in ['m3u', 'both']:
            m3u_path = output_dir / f"{original_stem}.m3u"
            with open(m3u_path, 'w', encoding='utf-8') as f:
                f.write(m3u_content)
            print(f"✓ Created {m3u_path.name}")
            files_created.append(m3u_path.name)
        
        # Create M3U8 if requested
        if playlist_format in ['m3u8', 'both']:
            m3u8_path = output_dir / f"{original_stem}.m3u8"
            with open(m3u8_path, 'w', encoding='utf-8') as f:
                f.write(m3u_content)
            print(f"✓ Created {m3u8_path.name}")
            files_created.append(m3u8_path.name)
        
        print("\n" + "="*70)
        print(f"MP3 Playlist Honeytoken(s) generated successfully!")
        print("="*70)
        print(f"\nFiles created in: {output_dir}")
        for filename in files_created:
            print(f"  • {filename}")
        print(f"\nHoneytoken UUID: {token_uuid}")
        print(f"\nNote: The playlist references: {original_filename}")
        print("   Make sure this file exists in the same directory!")
        
        return True

    except Exception as e:
        print(f"Error generating honeytoken: {e}")
        import traceback
        traceback.print_exc()
        return False