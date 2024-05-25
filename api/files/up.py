from fastapi import File, UploadFile, APIRouter
from session import Session, Track

router = APIRouter()


@router.post("/{session_id}/upload")
def upload(session_id: str, file: UploadFile = File(...)):
    s = Session.load(session_id)
    try:
        contents = file.file.read()
        t = Track("{}_track".format(session_id), 0.0, "", contents)
        s.add_track(t)
        s.save()
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    return {"message": f"Successfully uploaded {file.filename}"}
