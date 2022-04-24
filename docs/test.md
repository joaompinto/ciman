
The offical Docker registry API v2 does not provide detailed information about the "namespace" .

Based on:
    https://stevelasker.blog/2020/02/17/registry-namespace-repo-names/

    dns_name/namespace..../name:tag




docker run --rm gcr.io/go-containerregistry/crane --verbose pull bash latest
