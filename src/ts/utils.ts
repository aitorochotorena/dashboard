export
function baseUrl(): string {
    if ((document as any)._BASE_URL) {
        return (document as any)._BASE_URL as string;
    } else {
        return "/";
    }
}
