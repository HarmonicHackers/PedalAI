import os
from fastapi import File, UploadFile, APIRouter
from session import Session, Track

router = APIRouter()


@router.post("/{session_id}/upload")
def upload(session_id: str, file: UploadFile = File(...)):
    s = Session.load(session_id)
    try:
        contents = file.file.read()
        track_path = os.path.join(s.save_path, file.filename)
        t = Track("{}".format(file.filename), 0.0, "", contents, track_path)
        s.add_track(t)
        s.save()
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    return {"message": f"Successfully uploaded {file.filename}"}
