import itertools
import random
import json
# Word list and phrase database
words = []  # Initialize empty list for user input words


# Tạo data base chứa cụm từ
file_path = 'phrase.json'  # Path to the JSON file containing the phrase database
try:
    with open(file_path, 'r', encoding='utf-8') as file:
        hung_dict = json.load(file)
    error_message = ''
except Exception as e:
    hung_dict = None
    error_message = str(e)

# Tạo data base chứa từ và nhãn
file_path_data = 'word.json'  # Path to the JSON file containing the phrase database
try:
    with open(file_path_data, 'r', encoding='utf-8') as file:
        POS_dict = json.load(file)
    error_message = ''
except Exception as e:
    POS_dict = None
    error_message = str(e)

# phrase_database = {'Hung_ăn':1,
#                    'ăn_cơm':1,
#                    'Hung_ăn_cơm':1}  # Initialize empty dictionary for phrases and their probability


phrase_database = hung_dict  # Initialize empty dictionary for phrases and their probability

# Hàm sinh các hoán vị cho kịch bản 2 (Scenario 2)
def generate_permutations_2(words):
  permutations = []
  for permutation in itertools.permutations(words):
    # permutations.append(" ".join(permutation))
    permutations.append(permutation)
  return permutations


# Hàm sinh ra quần thể ban đầu
def generate_initial_population(words, population_size=10):
    return [random.sample(words, len(words)) for _ in range(population_size)]

# Order 1 Crossover
def crossover_order_1(parent1, parent2):
    start = random.randint(0, len(parent1) - 2)
    end = random.randint(start + 1, len(parent1) - 1)
    child = [None] * len(parent1)
    child[start:end + 1] = parent1[start:end + 1]

    tmp_parent2 = parent2.copy()
    for item in child[start:end + 1]:
        if item in tmp_parent2:
            tmp_parent2.remove(item)

    for item in tmp_parent2:
        for i in range(len(child)):
            if child[i] is None:
                child[i] = item
                break
    return child

# Function for Order 1 Crossover
def crossover_order_1_old(parent1, parent2,tmp):
    start = random.randint(0, len(parent1) - 2)
    end = random.randint(start + 1, len(parent1) - 1)
    # check start and end 
    for i in range(len(parent1)-1):
        tmp_sentence_2 = "_".join(words[i:i+2])
        if tmp_sentence_2 == tmp:
            start = i
            end = i+1
            break
    for i in range(len(parent1)-2):
        tmp_sentence_3 = "_".join(words[i:i+3])
        if tmp_sentence_3 == tmp:
            start = i
            end = i+2
            break
    
    child = [None] * len(parent1)
    child[start:end + 1] = parent1[start:end + 1]
    tmp_parent2 = parent2[start:end + 1]
    for item in child[start:end + 1]:
        if item in tmp_parent2:
            tmp_parent2.remove(item)
    for item in tmp_parent2:
        for i in range(len(child)):
            if child[i] is None:
                child[i] = item
                break
    return child


# Function for Order 1 Crossover
def crossover_order_1_update(parent1, parent2,tmp):
    start = random.randint(0, len(parent1) - 2)
    end = random.randint(start + 1, len(parent1) - 1)
    # check start and end 
    for i in range(len(parent1)-1):
        tmp_sentence_2 = "_".join(parent1[i:i+2])
        if tmp_sentence_2 == tmp:
            start = i
            end = i+1
            break
    for i in range(len(parent1)-2):
        tmp_sentence_3 = "_".join(parent1[i:i+3])
        if tmp_sentence_3 == tmp:
            start = i
            end = i+2
            break
    # print("tmp_sentence_2: ", tmp_sentence_2)
    # print("tmp_sentence_3: ", tmp_sentence_3)
    # print("start: ",start)
    # print("end: ",end)

    child = [None] * len(parent1)
    child[start:end + 1] = parent1[start:end + 1]
    tmp_parent2 = parent2.copy()
    for item in parent1[start:end + 1]:
        if item in tmp_parent2:
            tmp_parent2.remove(item)
            

    # print("tmp_parent2: ",tmp_parent2)
    for item in tmp_parent2:
        for i in range(len(child)):
            if child[i] is None:
                child[i] = item
                break
    return child


# Hàm lấy POStag
def get_pos(word):
    global POS_dict
    x =  POS_dict.get(word, [])
    print(x)
    return x

# Rule functions
def rule_verb_before_noun_or_pronoun(tags):
    for i in range(len(tags) - 1):
        if 'V' in tags[i] and ('N' in tags[i + 1] or 'P' in tags[i + 1]):
            return True
    return False

def rule1(tags):
    for i in range(len(tags) - 1):
        if ('N' in tags[i] or 'P' in tags[i] or 'Np' in tags[i]) and ('V' in tags[i + 1]):
            return True
    return False

def rule_verb_before_adjective(tags):
    for i in range(len(tags) - 1):
        if 'V' in tags[i] and 'A' in tags[i + 1]:
            return True
    return False

def rule_noun_before_adjective(tags):
    for i in range(len(tags) - 1):
        if 'N' in tags[i] and 'A' in tags[i + 1]:
            return True
    return False

def rule_class_noun_before_noun(tags):
    for i in range(len(tags) - 1):
        if 'Nc' in tags[i] and 'N' in tags[i + 1]:
            return True
    return False

def rule_common_noun_before_proper_noun(tags):
    for i in range(len(tags) - 1):
        if 'N' in tags[i] and 'Np' in tags[i + 1]:
            return True
    return False

def rule_unit_noun_before_singular_noun(tags):
    for i in range(len(tags) - 1):
        if 'Nu' in tags[i] and 'N' in tags[i + 1]:
            return True
    return False

def rule_adjective_after_noun(tags):
    for i in range(len(tags) - 1):
        if 'N' in tags[i] and 'A' in tags[i + 1]:
            return True
    return False

def rule_preposition_before_noun(tags):
    for i in range(len(tags) - 1):
        if 'E' in tags[i] and 'N' in tags[i + 1]:
            return True
    return False

def rule_interjection_at_start(tags):
    return 'I' in tags[0]

def rule_adverb_with_verb(tags):
    for i in range(len(tags) - 1):
        if 'R' in tags[i] and 'V' in tags[i + 1]:
            return True
    return False


def rule_determiner_before_noun(tags):
    for i in range(len(tags) - 1):
        if 'L' in tags[i] and 'N' in tags[i + 1]:
            return 1
    return 0

# Hàm đánh giá điểm ngữ pháp (Stage 1)
def evaluate_grammar(word_list, POS_dict):
    score = 0
    pos_tags = [get_pos(word) for word in word_list]
    print("pos: ", pos_tags)
    if rule1(pos_tags):
        score +=1

    # Check rule 1
    if rule_verb_before_noun_or_pronoun(pos_tags):
        score += 1

    # Check rule 2
    if rule_verb_before_adjective(pos_tags):
        score += 1

    # Check rule 3
    if rule_noun_before_adjective(pos_tags):
        score += 1

    # Check rule 4
    if rule_class_noun_before_noun(pos_tags):
        score += 1

    # Check rule 5
    if rule_common_noun_before_proper_noun(pos_tags):
        score += 1

    # Check rule 6
    if rule_unit_noun_before_singular_noun(pos_tags):
        score += 1

    # Check rule 7
    if rule_adjective_after_noun(pos_tags):
        score += 1

    # Check rule 8
    if rule_preposition_before_noun(pos_tags):
        score += 1

    # Check rule 9
    if rule_interjection_at_start(pos_tags):
        score += 1

    # Check rule 10
    if rule_adverb_with_verb(pos_tags):
        score += 1

    # Check rule 11
    score += rule_determiner_before_noun(pos_tags)

    return score*10


# Hàm tính điểm cho hoán vị
def evaluate_sentence(sentence):
  score = 0

  # Stage 1: Đánh giá ngữ pháp sử dụng luật
  global POS_dict
  score += evaluate_grammar(sentence, POS_dict)

  # Stage 2: Đánh giá dự trên số lần xuất hiện của cụm từ trong database
  # Tách câu thành những cụm 2 từ 3 từ
  phrases = []
  for i in range(len(sentence) - 1):
    phrases.append("_".join(sentence[i:i+2]))
  for i in range(len(sentence) - 2):
    phrases.append("_".join(sentence[i:i+3]))

  # thêm điểm nếu cụm từ xuất hiện trong database
  best_phrase = None
  for phrase in phrases:
    if phrase in phrase_database:
      # print("phrase: ",phrase, "score: ",phrase_database[phrase])
      score += phrase_database[phrase]
      # score += 1
      if best_phrase == None:
        best_phrase = phrase
      elif phrase_database[phrase] > phrase_database[best_phrase]:
        best_phrase = phrase

  return [score,best_phrase]



# Genetic algorithm (Scenario 3)
def genetic_algorithm(words, generations=100):
  # Step 1: Build initial population
  population = []

  population = generate_initial_population(words,generations)
  # print("initial population: ",population)
  # Step 2: Evaluate fitness and select parents
  best_individual_list = []
  best_individual = words
  for _ in range(100):
    print()
    print("Vòng lặp: ",_)
    # Calculate fitness for each individual in the population
    fitness_scores = [evaluate_sentence(sentence)[0] for sentence in population]
    best_phrases = [evaluate_sentence(sentence)[1] for sentence in population]

    # Select 2 individuals with the highest fitness
    # print("population_before: ",population)
    parents = []
    phrases_parents = []

    selected_parents = []
    for _ in range(10):
      max_index = fitness_scores.index(max(fitness_scores))
      selected_parents.append(population[max_index])
      phrases_parents.append(best_phrases[max_index])
      del population[max_index]
      del fitness_scores[max_index]

    # Step 3: Perform cross-breeding
    offspring = []
    for i in range(100):
      # Select two random parents from selected_parents
      parent1, parent2 = random.sample(selected_parents, 2)
      child = crossover_order_1(parent1, parent2)
      if child not in offspring:
        offspring.append(child)

    parent1,parent2 = selected_parents[:2]
    offspring.append(crossover_order_1_update(parent1, parent2,phrases_parents[0]))
    tmp = crossover_order_1_update(parent2, parent1,phrases_parents[1])
    if tmp not in offspring:
      offspring.append(crossover_order_1_update(parent2, parent1,phrases_parents[1]))

    # print("offspring: ",offspring)

    # Thêm 2 bố mẹ tốt nhất vào quần thể mới
    if parent1 not in offspring:
      offspring.append(parent1)
    if parent2 not in offspring:
      offspring.append(parent2)
    
    population = offspring
    # print("population_after: ",population)
    # print()

    # Thêm các cá thể tốt vào danh sách kết quả
    for individual in selected_parents[:2]:
      best_individual = individual
      print("best_individual: ",best_individual)

      if [best_individual,evaluate_sentence(best_individual)] not in best_individual_list:
        best_individual_list.append([best_individual,evaluate_sentence(best_individual)])

    print("best_individual_list: ",best_individual_list)

    # Điều kiện dừng
    if len(offspring) < 3:
      break

    # Đột biến
    i=0
    while i <10:
      tmp = random.sample(words, len(words))
      if tmp not in offspring:
        offspring.append(tmp)
        i+=1
    

  return best_individual_list

# Main program
# words = input("Enter words (separated by spaces): ").lower().split(" ")

# words = ['sáng','hôm','Hung','đi','ăn','giờ','qua','cơm','lúc','mười']
# words = ['Hung','đi','ăn','cơm','với','những', 'người','bạn','của','mình']
# words = [ 'bạn','ăn','cơm','Hung','đi','với']
words = ['nổi tiếng','trong','tôi','lớp','người','là']
words = ["nổi tiếng", "trong", "lớp", "người", "là", "tôi"]

words = ['người','là','tôi','đẹp','trai']
# words = ['Hung','đẹp trai', 'phong độ','và']
words = random.sample(words, len(words))
# words = ['của','bạn','ăn','cơm','Hung','đi','với','những', 'người','mình']
words = ["của", "bạn", "ăn", "cơm", "Hung", "đi", "với", "những", "người", "mình"]
# words = ['Một','giọt','nước','mắt','lăn','dài', 'trên','gò má','gầy','ốm','của','Lâm']
# words = ['nước','giọt','mắt','gò má','dài','lăn', 'của','trên','gầy','Một','ốm','Lâm']
# words = ['Hung','đi','ăn','cơm']
def solve(words):
    global POS_dict
    for word in words:
        if word not in POS_dict and (word[0].isupper() if word else False):
            POS_dict[word] = ['Np']

    if len(words) <= 5:
        # Scenario 2
        # Sinh ra tập các hoán vị 
        sentences = generate_permutations_2(words)

        # Tính toán từng hoán vị và trả về lits các cặp (câu,điểm)
        sentences_with_scores = [(sentence, evaluate_sentence(sentence)) for sentence in sentences]

        # Sắp xếp lại dãy kết quả 
        sorted_sentences = sorted(sentences_with_scores, key=lambda x: x[1], reverse=True)

        # Lấy 5 kết quả tốt nhất
        top_5_sentences = sorted_sentences[:5]

        # In ra kết quả ở terminal
        print("Top 5 Sentences with Highest Scores:")
        for sentence, score in top_5_sentences:
            print(f"Sentence: {' '.join(sentence)}, Score: {score}")

        # sorted_list = sorted(top_5_sentences, key=lambda x: x[1][0], reverse=True)
        return top_5_sentences

    else:
        # Scenario 3
        best_sentence = genetic_algorithm(words)
        # Sắp xếp lại theo thứ tự giảm dần của điểm
        sorted_list = sorted(best_sentence, key=lambda x: x[1][0], reverse=True)
        for sentence in sorted_list:
            print(f"Sentence: {' '.join(sentence[0])}, Score: {sentence[1][0]}, best_phrase: {sentence[1][1]}")  

        return sorted_list

# solve(words)
