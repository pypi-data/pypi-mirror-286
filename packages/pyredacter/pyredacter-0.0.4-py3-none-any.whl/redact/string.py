def redact_string(item: str) -> str:
    default = "*****"
    if len(item)<=4:
        return default
    start = f"{item[0]}{item[1]}"
    end = f"{item[len(item)-2]}{item[len(item)-1]}"
    stars = "*"*(len(item)-4)
    return f"{start}{stars}{end}"


if __name__ == "__main__":
    password = "testpassword"
    redacted = redact_string(password)

    if len(password) != len(redacted):
        print("lenghts did not match, probably off-by-one")

    print(f"{password} has been redacted to {redacted}")
