fun addParentheses(inputStr: String?): String {
    val strChars = inputStr!!.toCharArray()

    val strSize = strChars.size

    if (strSize == 1 || strSize == 2){
        return inputStr
    }

    if (strSize % 2 == 1) {
        val leftPartArr = strChars.sliceArray(0..strSize / 2 - 1)
        val center = strChars[strSize/2]
        val rightPartArr = strChars.sliceArray(strSize / 2 + 1..strSize - 1)

        val leftPartStr = leftPartArr.joinToString(postfix = "(", separator = "(")
        val centerStr = center.toString()
        val rightPartStr = rightPartArr.joinToString(prefix = ")", separator = ")")

        return leftPartStr + centerStr + rightPartStr

    } else {
        val leftPartArr = strChars.sliceArray(0..strSize / 2 - 1)
        val rightPartArr = strChars.sliceArray(strSize / 2..strSize - 1)

        val leftPartStr = leftPartArr.joinToString(separator = "(")
        val rightPartStr = rightPartArr.joinToString(separator = ")")

        return leftPartStr + rightPartStr

    }
}

fun main() {
    val inputStr: String? = readLine()
    println(addParentheses(inputStr))
}

