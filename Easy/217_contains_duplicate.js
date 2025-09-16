/**
 * @param {number[]} nums
 * @return {boolean}
 */
var containsDuplicate = function(nums) {
    let mySet = new Set();
    for (let e of nums) {
        if (mySet.has(e))
            return true;
        mySet.add(e);
    }
    return false;
};

console.log(containsDuplicate([1,2,3,4]));
console.log(containsDuplicate([1,2,3,1]));


// A one liner version
/**
 * @param {number[]} nums
 * @return {boolean}
 */
var containsDuplicate = function(nums) {
    return new Set(nums).size !== nums.length;
};

console.log(containsDuplicate([1,2,3,4]));
console.log(containsDuplicate([1,2,3,1]));