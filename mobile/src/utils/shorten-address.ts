export function shortenLibraAddress(address: string): string {
  const len = 6;
  return address.substr(0, len) + "...." + address.substr(len * -1);
}