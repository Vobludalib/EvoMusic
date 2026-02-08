import miditoolkit


def notes_to_midi(notes, out_path, ticks_per_beat=None, program=0, is_drum=False, name='Piano'):
    """Write a list of miditoolkit.Note objects to a .mid file.

    Args:
        notes (list): list of miditoolkit.Note instances
        out_path (str): path to write the .mid file
        ticks_per_beat (int|None): resolution for the MIDI file; if None uses library default
        program (int): MIDI program number for the instrument (0 = acoustic grand piano)
        is_drum (bool): whether the instrument is a drum channel
        name (str): instrument name
    """
    if ticks_per_beat is None:
        midi_obj = miditoolkit.MidiFile()
    else:
        # miditoolkit accepts `ticks_per_beat` as constructor kwarg
        midi_obj = miditoolkit.MidiFile(ticks_per_beat=ticks_per_beat)

    inst = miditoolkit.Instrument(program=program, is_drum=is_drum, name=name)

    # copy notes to avoid mutating caller's list and ensure they are sorted
    inst.notes = list(notes)
    try:
        inst.notes.sort(key=lambda n: n.start)
    except Exception:
        pass

    midi_obj.instruments.append(inst)

    midi_obj.dump(out_path)
