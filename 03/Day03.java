package aoc;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Objects;
import java.util.Set;
import java.util.stream.Collectors;
import java.util.stream.IntStream;
import java.util.stream.Stream;

public class Day03 {

    private static BufferedReader readInput(String day) throws FileNotFoundException {
        String path = System.getProperty("user.dir");
        File file = new File(path + "\\src\\aoc\\input" + day);
        BufferedReader br = new BufferedReader(new FileReader(file));
        return br;
    }
    
    private static HashMap<Character, Integer> calculateScores() {
        HashMap<Character, Integer> scores = new HashMap<Character, Integer>();
        for (int i = 65; i <= 122; i++) {
            char c = (char) i;
            if (i <= 90) {
                scores.put(c, i - 38);
            } else {
                scores.put(c, i - 96);
            }
        }
        return scores;
    }

    private static int calculateRuckSackPriority(String line, HashMap<Character, Integer> scores) {
        int border = line.length() / 2;
        Set<Character> first = line.substring(0, border)
                .chars()
                .mapToObj(c -> (char) c)
                .collect(Collectors.toSet());
        Set<Character> second = line.substring(border, line.length())
                .chars()
                .mapToObj(c -> (char) c)
                .collect(Collectors.toSet());
        char priority = first.stream()
                .filter(second::contains)
                .collect(Collectors.toSet())
                .stream()
                .findAny()
                .get();
        return scores.get(priority);
    }
    
    private static int calculateBadgePriority(ArrayList<String> rucksacks, HashMap<Character, Integer> scores) {
        Set<Character> first = rucksacks.get(0)
                .chars()
                .mapToObj(c -> (char) c)
                .collect(Collectors.toSet());
        Set<Character> second = rucksacks.get(1)
                .chars()
                .mapToObj(c -> (char) c)
                .collect(Collectors.toSet());
        Set<Character> third = rucksacks.get(2)
                .chars()
                .mapToObj(c -> (char) c)
                .collect(Collectors.toSet());
        char badge = first.stream()
                .filter(second::contains)
                .filter(third::contains)
                .collect(Collectors.toSet())
                .stream()
                .findAny()
                .get();

        return scores.get(badge);
    }
    
    private static ArrayList<ArrayList<String>> makeGroups(ArrayList<String> lines, int size) {
        IntStream indexStream = IntStream.range(0, lines.size());
        
        Stream<ArrayList<String>> groupStream = indexStream.mapToObj(i -> {
            int start = i * size;
            int end = Math.min(start + size, lines.size());

            if (end - start == size) {
                return new ArrayList<>(lines.subList(start, end));
            } else {
                return null;
            }
        }).filter(Objects::nonNull);

     return groupStream.collect(Collectors.toCollection(ArrayList::new));
    }

    public static void main(String[] args) {
        HashMap<Character, Integer> scores = calculateScores();
        ArrayList<String> lines = new ArrayList<String>();
        
        try {
            BufferedReader br = readInput("03");
            while (br.ready()) {
                lines.add(br.readLine());
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        
        ArrayList<ArrayList<String>> groups = makeGroups(lines, 3);
        
        int sumRucksackPriorities = lines.stream()
                .map(line -> calculateRuckSackPriority(line, scores))
                .reduce(0, Integer::sum);
        
        int sumBadgePriorities = groups.stream()
                .map(rucksacks -> calculateBadgePriority(rucksacks, scores))
                .reduce(0, Integer::sum);
        
        System.out.println("Part 1: " + sumRucksackPriorities);
        System.out.println("Part 2: " + sumBadgePriorities);
    }
}
