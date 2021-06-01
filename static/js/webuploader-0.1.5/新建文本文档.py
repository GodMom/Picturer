def normal(file_path, out):
    with open(file_path, 'r') as file:
        data = file.read()
    outstring = data.replace("{", "{\n").replace("}", "\n}\n\n").replace(";", ";\n")
    with open(out, 'w') as outfile:
        outfile.write(outstring)

    print("done!")


if __name__ == "__main__":
    normal('webuploader.min.js', 'webuploader.min1.js')
