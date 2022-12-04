package aoc;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Day04 {

    final static String REGEX = "(\\d+)-(\\d+),(\\d+)-(\\d+)";

    private static BufferedReader readInput(String day) throws FileNotFoundException {
        String path = System.getProperty("user.dir");
        File file = new File(path + "\\src\\aoc\\input" + day);
        BufferedReader br = new BufferedReader(new FileReader(file));
        return br;
    }

    private static ArrayList<Integer> parseLine(String line) {
        Pattern pattern = Pattern.compile(REGEX);
        Matcher matcher = pattern.matcher(line);
        ArrayList<Integer> sections = new ArrayList<Integer>();
        if (matcher.find()) {
            int sectionCount = matcher.groupCount();
            for (int i = 1; i <= sectionCount; i++) {
                int entry = Integer.parseInt(matcher.group(i));
                sections.add(entry);
            }
        }
        return sections;
    }

    private static boolean doesContain(ArrayList<Integer> sections) {
        int firstStart = sections.get(0);
        int firstEnd = sections.get(1);
        int secondStart = sections.get(2);
        int secondEnd = sections.get(3);
        return ((firstStart >= secondStart && firstEnd <= secondEnd)
                || (secondStart >= firstStart && secondEnd <= firstEnd));
    }

    private static boolean doesOverlap(ArrayList<Integer> sections) {
        int firstStart = sections.get(0);
        int firstEnd = sections.get(1);
        int secondStart = sections.get(2);
        int secondEnd = sections.get(3);

        return (doesContain(sections) || (firstStart <= secondStart && firstEnd >= secondStart)
                || (secondStart <= firstStart && secondEnd >= firstStart));
    }

    public static void main(String[] args) {
        ArrayList<String> lines = new ArrayList<String>();

        try {
            BufferedReader br = readInput("04");
            while (br.ready()) {
                lines.add(br.readLine());
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        
        int partOne = 0;
        int partTwo = 0;
        
        for (String line : lines) {
            ArrayList<Integer> sections = parseLine(line);
            if (doesContain(sections)) {
                partOne += 1;
            }
            if (doesOverlap(sections)) {
                partTwo += 1;
            }
        }
        System.out.println("Part 1: " + partOne);
        System.out.println("Part 2: " + partTwo);
    }

}