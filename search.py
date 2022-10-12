import sqlite3

class Search:

    _conn = sqlite3.connect('sales.sqlite')
    def department_total(self, dept):
        """
        Returns the sum of all sales within a department
        """
        cur = self._conn.cursor()
        returned = cur.execute('SELECT department, SUM(amount) as total FROM sales WHERE department = "' + dept + '";')
        return returned.fetchone()[1]

    def department_total_bydate(self, dept, date):
        """
        Returns the sum of all sales within a department on a specific date
        """
        cur = self._conn.cursor()
        returned = cur.execute("SELECT department, sale_date, SUM(amount) as total FROM sales WHERE department = '" + dept + "' AND sale_date = '" + date + "'")
        return returned.fetchone()[2]


    def country_count_date_range(self, country, start_date, end_date):
        """
        Returns the number of sales to buyers in a specific country between 2 dates, inclusive
        """
        cur = self._conn.cursor()
        returned = cur.execute("SELECT country, SUM(amount) as total,'" + start_date + "' AS first_sale, '" + end_date + "' AS last_sale FROM buyers JOIN sales ON buyers.id = sales.buyer_id WHERE country = '" + country + "' AND sale_date >= first_sale AND sale_date <= last_sale")
        return returned.fetchone()[1]

    def biggest_spender(self):
        """
        Returns a tuple with the first and last name of the buyer who spent the most money
        """
        cur = self._conn.cursor()
        returned = cur.execute("SELECT first_name, last_name, SUM(amount) as total FROM buyers JOIN sales ON buyers.id = sales.buyer_id GROUP BY buyer_id ORDER BY total DESC")
        to_return = returned.fetchone()
        return to_return[0], to_return[1]

    def biggest_spenders(self, how_many, department):
        """
        Returns the how_many highest spenders in a specific department
        """
        cur = self._conn.cursor()
        returned = cur.execute("SELECT first_name, last_name, SUM(amount) as total FROM buyers JOIN sales On buyers.id = sales.buyer_id WHERE department = '" + department + "' GROUP BY buyer_id ORDER BY total DESC LIMIT " + str(how_many))
        return returned.fetchall()
