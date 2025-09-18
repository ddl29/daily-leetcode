/**
 * @param {string} s
 * @return {boolean}
 */
var isPalindrome = function(s) {
    s = s.replace(/[^a-zA-Z0-9]/g, "").toLowerCase();

    let left = 0;
    let right = s.length-1;
    while (left < right) {
        if (s.charAt(left) !== s.charAt(right))
            return false;
        left++;
        right--;
    }
    return true;
};

console.log(isPalindrome("A man, a plan, a canal: Panama"));