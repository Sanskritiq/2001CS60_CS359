export const formatDate = (date) => {
    var hours = new Date(date).getHours();
    const minutes = new Date(date).getMinutes();
    const meridiem = hours < 12 ? 'AM' : 'PM';
    hours = hours % 12;
    return `${hours < 10 ? '0' + hours : hours}:${minutes < 10 ? '0' + minutes : minutes} ${meridiem}`;
}