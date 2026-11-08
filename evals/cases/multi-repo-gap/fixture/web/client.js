export async function status() { return (await fetch("/status")).json(); }
