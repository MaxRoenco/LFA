import { RegexGenerator } from "./RegexGenerator";
import { RegexParser } from "./RegexParser";
import { RegexTreePrinter } from "./RegexTreePrinter";

function main() {
    const patterns: string[] = [
        "(a|b)(c|d)E+G?", 
        "P(Q|R|S)T(UV|W|X)*Z+", 
        "1(0|1)*2(3|4){5}36"
    ];
    
    console.log("Roenco Maxim, Nr. 4:");
    console.log("Var. 1");
    
    for (let i = 0; i < patterns.length; i++) {
        console.log(`\n==== Pattern ${i+1}: ${patterns[i]} ====`);
        
        const regexParser = new RegexParser();
        const regexGenerator = new RegexGenerator(regexParser, 5, 50);
    
        const rootNode = regexParser.parseRegex(patterns[i]);
        
        const validCombinations = new Set(regexGenerator.generateValidCombinations(patterns[i]));
        
        console.log("\nGenerated valid combinations:");
        let count = 0;
        validCombinations.forEach(combo => {
            console.log(` - ${combo}`);
            count++;
            if (count === 10) {
                console.log(` ... and ${validCombinations.size - 10} more combinations`);
                return;
            }
        });
        
        console.log(`\nTotal valid combinations generated: ${validCombinations.size}`);
        
        const totalPossibleCombinations = regexGenerator.calculateTotalCombinations(patterns[i]);
        console.log(`Total possible combinations: ${totalPossibleCombinations}`);
        
        console.log(`\n--- Processing sequence for pattern ${i+1} ---`);
        console.log("Regex syntax tree:");
        console.log(RegexTreePrinter.visualize(rootNode));
        
        console.log("Explanation of pattern processing:");
        console.log(regexGenerator.explainPatternCombinations(patterns[i]));
        
        console.log("\n");
    }
}

main();