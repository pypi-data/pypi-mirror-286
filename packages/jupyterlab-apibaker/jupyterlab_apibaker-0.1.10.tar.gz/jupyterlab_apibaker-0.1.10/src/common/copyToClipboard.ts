
const copyToSystem = (clipboardData: string): void => {
     console.log(clipboardData);
     navigator.clipboard.writeText(clipboardData);
}

export default copyToSystem;
