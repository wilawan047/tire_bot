import os

folder = "."  # โฟลเดอร์ที่เก็บรูป

for filename in os.listdir(folder):
    new_name = filename.replace(" ", "_")  # แทน space ด้วย underscore
    new_name = new_name.replace("+", "")   # เอา + ออก ถ้ามี
    if filename != new_name:
        old_path = os.path.join(folder, filename)
        new_path = os.path.join(folder, new_name)
        os.rename(old_path, new_path)
        print(f"Renamed: {filename} -> {new_name}")
