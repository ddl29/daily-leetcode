/**
 * @param {string} s
 * @param {string} t
 * @return {boolean}
 */
var isAnagram = function(s, t) {
    return s.split("").sort().join("") === t.split("").sort().join("");
};
// n(log n)
console.log(isAnagram("anagram", "nagaram"));


// Another version but with O(n)
/**
 * @param {string} s
 * @param {string} t
 * @return {boolean}
 */
var isAnagram = function(s, t) {
    if (s.length !== t.length) return false;
    
    const count = {}

    for (let char of s) {
        count[char] = (count[char] || 0) + 1;
    }

    for (let char of t) {
        if (!count[char]) return false;
        count[char] = count[char] - 1;
    }

    return true;
};

console.log(isAnagram("anagram", "nagaram"));